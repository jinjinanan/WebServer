from werkzeug.wrappers import Request,Response
from werkzeug.local import LocalStack,LocalProxy

class framework(object):

    def __init__(self,package_name):
        self.package_name = package_name

    def run(self,host='localhost', port=5000, **options):
        from werkzeug import run_simple
        return run_simple(host,port,self,options)

    def wsgi_app(self,environ,start_response):
        request = Request(environ)
        text = 'hello world'
        response = Response(text, mimetype='text/plain')
        return response

    def __call__(self, environ,start_response):
        return self.wsgi_app(environ,start_response)
