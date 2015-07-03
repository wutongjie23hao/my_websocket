#web.py
#coding:utf8
__author__= "Xiaolei.Liang"

import threading
ctx = threading.local()

class HttpError(Exception):
    pass

class Request(object):
    
    def get(self, key, default=None):
        pass

    def input(self):
        pass

    @property
    def path_info(self):
        pass

    @property
    def headers(self):
        pass

    def cookie(self, name, default=None):
        pass

class Response(object):
    def set_header(self, key, value):
        pass

    def set_cookie(self, name, value, max_age=None,
                   expires=None, path='/'):
        pass

    @property
    def status(self):
        pass

    @status.setter
    def status(self, value):
        pass

def get(path):
    pass

def post(path):
    pass

def view(path):
    pass

def interceptor(pattern):
    pass

class TemplateEngine(object):
    def __call__(self, path, mode):
        pass

class JinJa2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(templ_dir),**kw)

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode("utf-8")

class WSGIApplication(object):
    def __init__(self, document_root=None, **kw):
        pass

    def add_url(self, func):
        pass

    def add_interceptor(self, func):
        pass

    @property
    def template_engine(self):
        pass

    @template_engine.setter
    deftemplate_engine(self,engine):
        pass

    def get_wsgi_application(self):
        def wsgi(env, start_response):
            pass
        return wsgi

    def run(self, port=9000, host='218.199.42.73'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application())
        server.serve_forever()

wsgi = WSGIApplication()
if __name__ == '__main__':
    wsgi.run()
else:
    applicaion = wsgi.get_wsgi_application()    

