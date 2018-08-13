
from werkzeug.wrappers import Request,Response
from werkzeug.routing import Map, Rule
from werkzeug.local import LocalStack,LocalProxy

class CusResponse(Response):
    default_mimetype = 'text/html'

class framework(object):

    def __init__(self,package_name):
        self.package_name = package_name
        self.debug = False
        self.view_functions = {}
        # 路由
        self.url_map = Map()

    def run(self,host='localhost', port=5000, **options):
        from werkzeug import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host,port,self,options)

    def dispatch_request(self):
        pass

    def wsgi_app(self,environ,start_response):
        request = Request(environ)
        response = CusResponse('hello world \n')
        return response(environ,start_response)

    def route(self,rule, **options):
        def decorator(f):
            if 'endpoint' is not options:
                options['endpoint'] = f.__name__
            self.url_map.add(Rule(rule,**options))
            self.view_functions[options['endpoint']] = f
            return f
        return decorator

    def __call__(self, environ,start_response):
        return self.wsgi_app(environ,start_response)



