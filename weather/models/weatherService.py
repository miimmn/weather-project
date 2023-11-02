import pandas as pd
import datetime as dt
import requests
import json
from config import APIkey
from config import getLogger


class weatherService:

    def __init__(self) :
        self.logger = getLogger()


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
        # 일치하는 주소 없을 때
        if not xyPoint :
            return "NO DATA"

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
        key = APIkey

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

        self.logger.info("  날짜  :  " + param['base_date'])
        self.logger.info("  시간  :  " + param['base_time'])

        try : 
            res = requests.get(url, params=param)
            res_json = json.loads(res.content)
            items = res_json['response']['body']['items']['item']

        except:
            self.logger.info("  API 호출 중 예외 발생......  ")

            if res_json['response']['header']['resultCode'] == '01' :
                self.logger.info("  base_date 혹은 base_time 요청 파라미터가 잘못 되었습니다.  ")

            elif res_json['response']['header']['resultCode'] == '03' :
                self.logger.info("  위치정보 파라미터 nx, ny 에 해당하는 데이터는 기상청에서 제공되지 않는 데이터입니다.  ")

            elif res_json['response']['header']['resultCode'] == '11' :
                self.logger.info("  필수 요청 파라미터가 누락 되었습니다.  ")

            return []
        return items


    # 기온 그래프용 데이터
    def getTemperature(self, data):

        # 기온만 가져오기
        temperature = []
        for i in data :
            temp = {}
            if i['category'] == 'TMP' :
                temp['temperature'] = int(i['fcstValue'])
                temp['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]

                temperature.append(temp)

        return temperature


     # 습도 그래프용 데이터
    def getHumidity(self, data):

        # 습도만 가져오기
        humidity = []
        for i in data :
            hum = {}
            if i['category'] == 'REH' :
                hum['humidity'] = int(i['fcstValue'])
                hum['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]

                humidity.append(hum)
        
        return humidity
    

    # 날씨 상태 데이터 (ex - 맑음, 흐림...)
    def getWeatherStatus(self, data) :

        sky = [] # 하늘 상태
        pty = [] # 강수 형태
        result = []

        for i in data :
            temp = {}
            if i['category'] == 'SKY' :
                temp['sky'] = int(i['fcstValue'])
                temp['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]
                sky.append(temp)

            elif i['category'] == 'PTY' :
                temp['pty'] = int(i['fcstValue'])
                temp['fcstTime'] = i['fcstDate'][4:]+"/"+i['fcstTime'][:2]
                pty.append(temp)

            
        for s, p in zip(sky, pty) : 
            temp = {}
            temp['sky'] = s['sky']
            temp['pty'] = p['pty']
            temp['fcstTime'] = p['fcstTime']

            result.append(temp)


        # sky, pty값 하나로 통일 (맑음, 구름많음, 흐림, 눈, 비)
        status = []
        skyString = [' ', '맑음', ' ', '구름많음', '흐림']
        ptyString = [' ', '비', '진눈깨비', '눈']

        for i in result :
            temp = {}

            self.logger.info("    강수 형태 값 :  " + str(i['pty']))

            if i['pty'] in (0, '-',' null') :
                temp['status'] = skyString[i['sky']]
            else :
                temp['status'] = ptyString[i['pty']]

                # 소나기 값 == 4인데 비(1)와 동일값으로 취급
                if i['pty'] == 4 :
                    temp['status'] = ptyString[1]
            
            temp['fcstTime'] = i['fcstTime']
            status.append(temp)

        return status


    # 그래프용 데이터 (기온, 습도, 날짜&시간대)
    def getWeather(self, address) :

        # API 호출 데이터 가져오기
        data = self.getWeatherByAPI(address)
        if data == "NO DATA" :
            return "NO DATA"

        # 그래프용 데이터 가공
        temperature =self.getTemperature(data)
        humidity = self.getHumidity(data)
        weatherStatus = self.getWeatherStatus(data)

        result = []
        for t, h, s in zip(temperature, humidity, weatherStatus) :
            temp = {}
            
            temp['temperature'] = t['temperature']
            temp['humidity'] = h['humidity']
            temp['fcstTime'] = t['fcstTime']
            temp['status'] = s['status']

            result.append(temp)
        
        return result
