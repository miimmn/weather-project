import cherrypy
from history.models.searchHistoryService import searchHistoryService
from config import access_check
import os

class searchHistoryController() :

    def __init__(self) :
        self.svc = searchHistoryService()
        self.path = os.path.dirname(os.path.abspath(__file__))

    # 검색 기록 페이지 - GET
    @cherrypy.expose
    @access_check
    def index(self) :
        return open(self.path + '/search_history.html')
    

    # 검색 기록 화면으로 보내기 - GET
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @access_check
    def getSearchHistory(self) :
        email = {}
        email['user_email'] = cherrypy.session['userEmail']

        history = self.svc.getSearchHistory(email)
        return history
    
    
    # 검색 기록 삭제
    @cherrypy.expose
    # def deleteSearchHistory(self, **data) :
    def deleteSearchHistory(self, id) :
        data = {}
        data['history_id'] = id
        self.svc.deleteSearchHistory(data)
