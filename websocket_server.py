# -*- coding: utf8 -*-
#!/usr/bin/env python
__author__='Xiaolei.Liang'

import socket
import threading
import sys
import os
import base64
import hashlib
import struct
# ======= config ======
HOST = '218.199.42.73'
PORT = 3372
MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n"\
                   "Connection: Upgrade\r\n"\
                   "Sec-WebSocket-Accept: {1}\r\n"\
                   "WebSocket-Location: ws://{2}/tt.html\r\n"\
                   "WebSocket-Protocol:chat\r\n\r\n"
MAX_BUFUR_SIZE = 1024

connectionlist = {}

def send_data(connection, data):
    if data:
        data = str(data)
    else:
        return False
    token = "\x81"
    length = len(data)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
    data = '%s%s' % (token, data)
    connection.send(data)
    return True

def first_login(data):
    global connectionlist
    try:
        username = data.split(":",1)[1].strip()
    except:
        username = data
    if data and connectionlist:
        data = '欢迎【%s】进入聊天室！' % username
        for key,value in connectionlist.iteritems():
            send_data(value, data)
            
def message_broadcast(data):
    global connectionlist
    for key,value in connectionlist.iteritems():
        send_data(value, data)

def delete_connection(item):
    global connectionlist
    del connectionlist['connection'+item]

class Th(threading.Thread):
    def __init__(self, connection, index, name, remote, path="/"):
        threading.Thread.__init__(self)
        self.con = connection
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""

    def run(self):
        print 'Socket %s Start!' % self.index
        self.handshaken = False
        while True:
            try:
                data = self.recv_data(MAX_BUFUR_SIZE)
                if self.handshaken == False:
                    #self.handshake()
                    self.handshaken = True
                    if data:
                        first_login(data)
                        print "%s:" % self.name,data.decode("utf8")
                else:
                    if data:
                        message_broadcast(data)
                        print "%s:" % self.name,data.decode("utf8")
                    else:
                        repr(data)
                        self.con.close()
                        delete_connection(str(self.index))
                        break
            except:
                self.con.close()
                delete_connection(str(self.index))
                break
        print '%s end...' % self.name

    def recv_data(self, num):
        try:
            all_data = self.con.recv(num)
            if not len(all_data):
                return False
            else:
                code_len = ord(all_data[1])&127
                if code_len == 126:
                    masks = all_data[4:8]
                    data = all_data[8:]
                elif code_len == 127:
                    masks = all_data[10:14]
                    data = all_data[14:]
                else:
                    masks = all_data[2:6]
                    data = all_data[6:]
                raw_str = ""
                i = 0
                for d in data:
                    raw_str += chr(ord(d)^ord(masks[i%4]))
                    i += 1
                return raw_str
        except:
            return False

    def handshake(self):
        headers = {}
        shake = self.con.recv(1024)

        if not len(shake):
            return False
        #print shake
        header, data = shake.split('\r\n\r\n',1)
        for line in header.split('\r\n')[1:]:
            key, val = line.split(':', 1)
            headers[key] = val

        if 'Sec-WebSocket-Key' not in headers:
            print ('This socket is not websocket, client close.')
            self.con.close()
            return False
            
        sec_key = headers['Sec-WebSocket-Key'].strip()
        #print 'sec_key:',sec_key
        res_key = base64.b64encode(hashlib.sha1(sec_key + MAGIC_STRING).digest())

        str_handshake = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}',HOST+':'+str(PORT))
        #print str_handshake
        self.con.send(str_handshake)
        return True
    
def handshake(con):
    headers = {}
    shake = con.recv(1024)
    if not len(shake):
        return False
    header, data = shake.split('\r\n\r\n',1)
    for line in header.split('\r\n')[1:]:
        key, val = line.split(':', 1)
        headers[key] = val
    if 'Sec-WebSocket-Key' not in headers:
        print ('This socket is not websocket, client close.')
        con.close()
        return False       
    sec_key = headers['Sec-WebSocket-Key'].strip()
    res_key = base64.b64encode(hashlib.sha1(sec_key + MAGIC_STRING).digest())
    str_handshake = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}',HOST+':'+str(PORT))
    con.send(str_handshake)
    return True

class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
        try:
            self.socket.bind(('%s' % HOST, PORT))
            self.socket.listen(100)
            print "WebSocketServer Start:bind %s, ready to use" % str(PORT)
        except:
            print("Server error, quit")
            self.socket.close()
            sys.exit()
        global connectionlist
        i = 0
        while True:
            connection, address = self.socket.accept()
            print "Got connection from ", address
            try:
                username=address[0]
                if handshake(connection):
                    newSocket = Th(connection, i, username, address)
                    newSocket.start()
                    connectionlist['connection'+str(i)] = connection
                    i = i+1
            except Exception, e:
                print 'start new thread error:', e
                connection.close()
            print "now have %s connections!" % str(len(connectionlist))

if __name__ == '__main__':
    #new_service()
    #pass
    server = WebSocketServer()
    server.begin()
    print 'end....'

