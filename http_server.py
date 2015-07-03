#http_server.py
#coding:utf8
__author__='Xiaolei.Liang'

from wsgiref.simple_server import make_server

#======config======
HOST='218.199.42.73'
PORT=8000

def application(environ, start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    try:
        server_buffer=""
        with open('client_copy.html','rb') as f:
            for line in f:
                server_buffer += line
        return server_buffer
    except Exception,e:
        print e
        return "<h4>请刷新</h4>"

httpd = make_server('%s' % HOST, PORT, application)
print "Serving HTTP on port %s..." % str(PORT)

httpd.serve_forever()

