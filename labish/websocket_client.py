#
#coding:utf-8

import socket
PORT = 9911

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket()
sock.connect(("127.0.0.1",9911))
try:
    sock.send('''
GET /demo HTTP/1.1 \r
Host: localhost \r
Connection: Upgrade \r
Sec-WebSocket-Key2: 12998 5 Y3 1 .P00 \r
Upgrade: WebSocket \r
Sec-WebSocket-Key1: 4@1 46546xW%0l 1 5 \r
Origin: http://127.0.0.1:9911 \r
\x43
'''.strip()+'\r\n\r\n' )

    data = sock.recv(8899)
    print data
finally:
    sock.close()
