import cherrypy
from models.services.userService import userService


class userController():

    def __init__(self):
        self.svc = userService()

    # 로그인 화면
    @cherrypy.expose
    def loginview(self):
        return open('./templates/login.html')

    # 로그인
    @cherrypy.expose
    def login(self, **kwargs) :

        # 성공 시 사용자 정보(이메일, 이름)
        # 실패 시 error 메시지 반환
        returnValue = self.svc.login(kwargs)

        cherrypy.session.pop('userEmail', None)
        cherrypy.session.pop('userName', None)

        # DB에 값이 존재하는 경우
        if type(returnValue) == type([]) :

            print("로그인 성공  ....... ")

            cherrypy.session['userEmail'] = kwargs['email']
            cherrypy.session['userName'] = returnValue[1]

        # 입력 정보가 틀린 경우
        elif returnValue == "FAIL" :
            print(" 로그인 실패 : 정보 불일치 ")
            cherrypy.response.status = 403
            # return cherrypy.HTTPError(401, '로그인 정보가 일치하지 않습니다.')

        # 가입되지 않은 사용자일 경우
        elif returnValue == "NO EXIST" :
            print(" 로그인 실패 : 가입되지 않은 이메일 ")
            cherrypy.response.status = 401

    
    # 로그아웃
    @cherrypy.expose
    def logout(self) : 
        cherrypy.session.pop('userEmail', None)
        cherrypy.session.pop('userName', None)
        

    # 회원가입 화면
    @cherrypy.expose
    def signupview(self) :
        # 데이터 받아온 걸로 회원 등록
        return open('./templates/signup.html')

    # 회원가입
    @cherrypy.expose
    def signup(self, **params) :
        self.svc.signup(params)