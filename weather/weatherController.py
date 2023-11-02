import cherrypy
from weather.models.weatherService import weatherService
from history.models.searchHistoryService import searchHistoryService
from history.models.searhHistoryDAO import searchHistoryDAO
from config import access_check
import datetime as dt
import os

class weatherController():

    def __init__(self):
        self.svc = weatherService()
        self.dao = searchHistoryDAO()
        self.path = os.path.dirname(os.path.abspath(__file__))


    # 메인 화면
    @cherrypy.expose
    @access_check
    def index(self):
        return open(self.path + '/weather.html')


    # GET - 날씨 예보 조회
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @access_check
    def getweather(self, **kwargs):

        insertInfo = kwargs
        insertInfo['user_email'] = cherrypy.session['userEmail']
        insertInfo['history_date'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #2023-10-30
        
        result = self.svc.getWeather(kwargs)
        
        if not result == "NO DATA" :
            self.dao.insertSearchHistory(insertInfo) # 검색 기록 저장
            return result
        else :
            cherrypy.response.status = 400
