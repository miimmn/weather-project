import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'))

import json

class searchHistoryController() :

    @cherrypy.expose
    def getsearchhistory() :
        template = env.get_template('index.html')
        user = [{"key" : '앗뇽하세요'}, {"key" : '앗뇽하세요'}, {"key" : '앗뇽하세요'}]
        

        return template.render(myData = user)