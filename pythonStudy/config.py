from os.path import abspath


CP_CONF = {
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/css',
        'tools.staticdir.root': '/opt/py-project'
    },

    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/js',
        'tools.staticdir.root': '/opt/py-project'
    }

}

SERVER_CONF = {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8081,
    
    'tools.sessions.on': True,
    'tools.sessions.storage_type': "File",
    'tools.sessions.storage_path': 'sessions',
    'tools.sessions.timeout': 10
}


# API용 KEY
keys = 'dea5nrDMUzQXecyXltQeEeyEEhqOTeFF0eTmHVSZn9v9PDgHrmrOsgRYjrkBHuUIQ4j%2BojRmLBb2Sl6SFh3Ufw%3D%3D'

