import pandas as pd
import datetime as dt
import requests
import json


class weatherService:

    def __init__(self) -> None:
        pass

    # pandas 사용
    # 주소로 위경도 변환
    def geoTranslate(self, data):

        df = pd.read_csv('etc/위경도.csv')

        df = df[['1단계', '2단계', '3단계', '격자 X', '격자 Y']]
        df = df[(df['1단계'] == data['si']) & 
                (df['2단계'].str.contains(data['gu']) &
                 df['3단계'].str.contains(data['dong'][0:-1]))]
        
        result = df.to_dict('records')

        return result


    # base_time 계산
    def cal_baseTime(self, origin) :

        base_time = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']
            
        for i, v in enumerate(base_time) :
            if(origin < v) :
                # 0200 보다 이전일 때 케이스 처리하기 (전날 2300)
                if i == 0 :
                    return base_time[-1]
                else :
                    return base_time[i-1]
            
        return base_time[-1]
    

    # API 호출하여 데이터 받아오기
    def getWeatherByAPI(self, address) :

        # 주소로 x, y 좌표 가져오기
        xyPoint = self.geoTranslate(address)
        x = dt.datetime.now()
        now = x.strftime("%H%M")
        basetime = self.cal_baseTime(now)


        if now < basetime :
            # 전날을 기준으로 함
            basedate = (dt.date.today() - dt.timedelta(1)).strftime("%Y%m%d")
        else :
            basedate = x.strftime("%Y%m%d")
        
        # 단기예보
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        key = 'dea5nrDMUzQXecyXltQeEeyEEhqOTeFF0eTmHVSZn9v9PDgHrmrOsgRYjrkBHuUIQ4j+ojRmLBb2Sl6SFh3Ufw=='

        param = {
            'serviceKey' : key,
            'pageNo' : '1', 
            'numOfRows' : '600', 
            'dataType' : 'JSON',
            'base_date' : basedate, 
            'base_time' : basetime, 
            'nx': str(xyPoint[0]['격자 X']), 
            'ny' : str(xyPoint[0]['격자 Y'])
        }

        print("날짜  :  ",param['base_date'])
        print("시간  :  ",param['base_time'])


        try : 
            res = requests.get(url, params=param)
            res_json = json.loads(res.content)
            items = res_json['response']['body']['items']['item']

        except:
            print("API 호출 중 예외 발생......")

            if res_json['response']['header']['resultCode'] == '01' :
                print("base_date 혹은 base_time 요청 파라미터가 잘못 되었습니다.")

            elif res_json['response']['header']['resultCode'] == '03' :
                print("위치정보 파라미터 nx, ny 에 해당하는 데이터는 기상청에서 제공되지 않는 데이터입니다.")

            elif res_json['response']['header']['resultCode'] == '11' :
                print("필수 요청 파라미터가 누락 되었습니다.")

            return []


        return items


    # 기온 그래프용 데이터
    def getTemperature(self, address):

        item = self.getWeatherByAPI(address)

        # 기온만 가져오기
        temperature = []
        for i in item :
            temp = {}
            if i['category'] == 'TMP' :
                temp['temperature'] = int(i['fcstValue'])
                temp['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]

                temperature.append(temp)

        return temperature


     # 습도 그래프용 데이터
    def getHumidity(self, data):

        item = self.getWeatherByAPI(data)

        # 습도만 가져오기
        humidity = []
        for i in item :
            hum = {}
            if i['category'] == 'REH' :
                hum['humidity'] = int(i['fcstValue'])
                hum['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]

                humidity.append(hum)
            
        return humidity
    

    # 그래프용 데이터 (기온, 습도, 날짜&시간대)
    def getWeather(self, address) :

        temperature =self.getTemperature(address)
        humidity = self.getHumidity(address)

        result = []
        for t, h in zip(temperature, humidity) :
            temp = {}
            if t['fcstTime'] == h['fcstTime'] :
                temp['temperature'] = t['temperature']
                temp['humidity'] = h['humidity']
                temp['fcstTime'] = t['fcstTime']

                result.append(temp)
        
        return result
