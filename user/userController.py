import cherrypy
from user.models.userService import userService
from config import getLogger
import os

class userController():

    def __init__(self):
        self.svc = userService()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.logger = getLogger()


    # 로그인 화면
    @cherrypy.expose
    def loginview(self):
        return open(self.path + '/login.html')

    # 로그인
    @cherrypy.expose
    def login(self, **kwargs) :

        # 성공 시 사용자 정보(이메일, 이름)
        # 실패 시 status error 반환
        returnValue = self.svc.login(kwargs)

        cherrypy.session.pop('userEmail', None)
        cherrypy.session.pop('userName', None)

        # DB에 값이 존재하는 경우

        # 입력 정보가 틀린 경우
        if returnValue == "FAIL" :
            self.logger.info("  로그인 실패 : 정보 불일치  ")
            cherrypy.response.status = 403

        # 가입되지 않은 사용자일 경우
        elif returnValue == "NO EXIST" :
            self.logger.info("  로그인 실패 : 가입되지 않은 이메일  ")
            cherrypy.response.status = 401

        elif returnValue != ['',''] :
            self.logger.info("로그인 성공 ........" + str(returnValue))
            cherrypy.session['userEmail'] = kwargs['email']
            cherrypy.session['userName'] = returnValue[1]

    
    # 로그아웃
    @cherrypy.expose
    def logout(self) : 
        cherrypy.session.pop('userEmail', None)
        cherrypy.session.pop('userName', None)


    # 회원가입 화면
    @cherrypy.expose
    def signupview(self) :
        return open(self.path + '/signup.html')

    # 회원가입
    @cherrypy.expose
    def signup(self, **params) :
        result = self.svc.signup(params)
        if result == "ALREADY EXIST" :
            cherrypy.response.status = 400

        