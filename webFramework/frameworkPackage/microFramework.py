from werkzeug.wrappers import Request,Response
from werkzeug.local import LocalStack,LocalProxy

class CusResponse(Response):
    default_mimetype = 'text/html'

class framework(object):

    def __init__(self,package_name):
        self.package_name = package_name
        self.debug = False

    def run(self,host='localhost', port=5000, **options):
        from werkzeug import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host,port,self,options)

    def wsgi_app(self,environ,start_response):
        request = Request(environ)
        response = CusResponse('hello world \n')
        return response(environ,start_response)

    def __call__(self, environ,start_response):
        return self.wsgi_app(environ,start_response)

