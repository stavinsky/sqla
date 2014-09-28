import cherrypy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Sqla(cherrypy.Tool):
    _name = 'sqla'
    _engine = None
    conf = None
    sessions = dict()
    def __init__(self):
        pass

    def _setup(self):
        if cherrypy.request.config.get('tools.staticdir.on', False) or \
                cherrypy.request.config.get('tools.staticfile.on', False):
            return
        self.conf = self._merged_args()
        cherrypy.request.hooks.attach('on_start_resource', self.on_start_resource)
        cherrypy.request.hooks.attach('on_end_resource', self.on_end_resource)

    def get_engine(self):
        if self._engine is None:
            engine = create_engine(self.conf['uri'], echo=self.conf.get('echo'))
            self._engine = engine
        return self._engine

    def get_session(self):


        if not hasattr(cherrypy.thread_data, 'db_session'):
            session_factory = sessionmaker(autoflush=True, autocommit=False, bind=self.get_engine())
            Session = scoped_session(session_factory)
            cherrypy.thread_data.db_session = Session()

        return cherrypy.thread_data.db_session

    def on_start_resource(self):
        cherrypy.request.sql_session = self.get_session()

    def on_end_resource(self):
        """
        I tryed to close sessions here but, if I close session here I have to open it again on next request.
        There is only few sessions are opened during all application life. Value of opened value set in
        server.thread_pool. So I don't undarstand now where I have to close sessions. Probably on thread_stop
        """
        pass
