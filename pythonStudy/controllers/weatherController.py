import cherrypy
from models.services.weatherService import weatherService


class weatherController():

    def __init__(self):
        self.svc = weatherService()

    # 메인 화면
    @cherrypy.expose
    def index(self):
        # cherrypy.response.headers['Content-Type'] = 'text/plain'

        return open('./templates/index.html')


    # GET - 날씨 예보 조회
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getweather(self, **kwargs):
    
        return self.svc.getWeather(kwargs)
