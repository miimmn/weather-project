import cherrypy
import random
import string
import config
from controllers.weatherController import weatherController
from controllers.userController import userController
from controllers.searchHistoryController import searchHistoryController


class MyApp:
    def __init__(self):
        self.weatherController = weatherController()
        self.userController = userController()
        self.searchHistoryController = searchHistoryController()

    def configure(self):
        # 애플리케이션 루트 URL 경로 설정
        cherrypy.tree.mount(self.weatherController, '/weather', config=None)
        cherrypy.tree.mount(self.userController, '/user', config=None)
        cherrypy.tree.mount(self.searchHistoryController, '/history', config=None)


        # # applicaton config is provided
        # cherrypy.tree.mount(Token(), '/token', {'/' : {
        #     'tools.sessions.on' : True,
        #     'tools.json_out.on' : True,
        # }})


        cherrypy.config.update(config.SERVER_CONF)



if __name__ == '__main__':
    my_app = MyApp()
    my_app.configure()

    cherrypy.quickstart(my_app, '/', config=config.CP_CONF)



# class Token:

#   @cherrypy.expose
#   def csrf(self):
#     crsf = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
#     cherrypy.session['csrf'] = crsf
#     return {'crsf': crsf}