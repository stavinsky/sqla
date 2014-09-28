sqla
====

cherrypy sqlalchemy tool

This is simple cherrypy tool for cherrypy 

simple using example

config
------
```
from sqla import Sqla
from root import Root


app_conf = {'/':
                 {
                     'tools.sqla.on': True,
                     'tools.sqla.uri': db_url,
                 }
}


if __name__ == "__main__":

    cherrypy.tools.sqla = Sqla()
    

    cherrypy.tree.mount(root=Root, config=app_conf, script_name='/')

    cherrypy.server.socket_host = ip
    cherrypy.server.socket_port = port

    cherrypy.engine.start()
    cherrypy.engine.block()

```

usage
-----

```
class Root():
    def index(self):
        session = cherrypy.request.sql_session
        ...
        
```
