import cherrypy
import config
from weather.weatherController import weatherController
from user.userController import userController
from history.searchHistoryController import searchHistoryController


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

        cherrypy.config.update(config.SERVER_CONF)


if __name__ == '__main__':
    my_app = MyApp()
    my_app.configure()

    cherrypy.quickstart(my_app, '/', config=config.CP_CONF)


