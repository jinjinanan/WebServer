
from werkzeug.wrappers import Request,Response
from werkzeug.routing import Map, Rule
from werkzeug.local import LocalStack,LocalProxy
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.exceptions import HTTPException
from six import string_types
import threading
class CusRequest(Request):
    def __init__(self):
        super().__init__()
        self.endpoint = None
        self.view_args = None


class CusResponse(Response):
    default_mimetype = 'text/html'

class _RequestContext(object):
    def __init__(self,app,environ):
        self.app = app
        self.request = app.request_class
        self.response = app.response_class
        self.url_adapter = app.url_map.bind_to_environ(environ)
        # self.session = app.open_session(self.request)


class framework(object):

    request_class = CusRequest

    response_class = CusResponse

    secret_key = None

    session_cookie_name = 'session'

    def __init__(self,package_name):
        self.package_name = package_name
        self.debug = False
        self.view_functions = {}
        # 路由
        self.url_map = Map()

    # def open_session(self,request):
    #     key = self.secret_key
    #     if key is not None:
    #         return SecureCookie.load_cookie(request,self.session_cookie_name,secret_key=key)
    #
    # def save_session(self,session,response):
    #     if session is not None:
    #         session.save_cookie(response,self.session_cookie_name)

    def run(self,host='localhost', port=5000, **options):
        from werkzeug import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host,port,self,options)


    #  处理请求
    def match_request(self):
        try:
            rv = _request_ctx_stack.top.url_adapter.match()
            request.endpoint, request.view_args = rv  # ('index', {})
            return rv
        except HTTPException:
            print('1')
        except Exception:
            print('2')


    def dispatch_request(self):
        endpoints,values = self.match_request()
        return self.view_functions[endpoints](**values)

    def make_response(self,rv):
        if isinstance(rv,self.response_class):
            return rv
        if isinstance(rv,string_types):
            return self.response_class(rv)


    def process_response(self,response):
        # session = _request_ctx_stack.top.session
        # if session is not None:
        #     self.save_session(session,response)
        pass



    def wsgi_app(self,environ,start_response):
        """
        :param environ:
        :param start_response:
        :return:
        实际的标准wsgi客户端函数
        """
        _request_ctx_stack.push(_RequestContext(self, environ))
        try:
            rv = self.dispatch_request()
            response = self.make_response(rv)
            return response(environ,start_response)
        finally:
            _request_ctx_stack.pop()


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


_request_ctx_stack = LocalStack()
request = LocalProxy(lambda :_request_ctx_stack.top.request)
# session = LocalProxy(lambda :_request_ctx_stack.top.session)
