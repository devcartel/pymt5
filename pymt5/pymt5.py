# -*- coding: utf-8 -*-
#
# Copyright (C) DevCartel Co.,Ltd.
# Bangkok, Thailand
#
import socket
import threading
from six.moves import socketserver
import re
import time
from collections import OrderedDict

MSG_SEPARATOR               = '\n'
MSG_SEPARATOR_TAG           = '\x01'
MSG_SEPARATOR_TAGVALUE      = '='
MSG_MAX_SIZE                = 4096

socketserver.TCPServer.allow_reuse_address = True

__all__ = ['PyMT5']

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur_thread = threading.current_thread()
        requests = self.server.requests
        if self.request not in requests:
            requests[self.request] = {'client_id':cur_thread.ident,
                                      'client_address':self.client_address[0],
                                      'client_port':self.client_address[1]}
            if callable(self.server.onConnected):
                self.server.onConnected(requests[self.request])
        buffer = b''
        while True:
            try:
                part = self.request.recv(MSG_MAX_SIZE)
                if not part: break
                buffer += part
                if len(part) < MSG_MAX_SIZE:
                    for decoded in buffer.decode('utf-8').split(MSG_SEPARATOR):
                        data = OrderedDict(re.findall("(.*?)"+MSG_SEPARATOR_TAGVALUE+"(.*?)"+MSG_SEPARATOR_TAG, decoded))
                        if data and callable(self.server.onData):
                            data.update({'client_id':cur_thread.ident})
                            self.server.onData(data)
                    buffer = b''
            except socket.error:
                break
        if callable(self.server.onDisconnected) and (self.request in requests):
            self.server.onDisconnected(requests[self.request])
        self.request.close()

class PyMT5(socketserver.ThreadingTCPServer):
    def __init__(self, host='', port=16838, *args, **kwargs):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), ThreadedTCPRequestHandler)
        self.requests = {}
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.setDaemon(True)
        self.server_thread.start()
        self.onConnected = None
        self.onDisconnected = None
        self.onData = None

    def stop(self):
        for request in list(self.requests):
            self.shutdown_request(request)
        self.shutdown()
        self.server_close()

    def broadcast(self, data):
        msg = ''
        for k,v in data.items():
            msg += k+MSG_SEPARATOR_TAGVALUE+v+MSG_SEPARATOR_TAG
        for request in list(self.requests):
            try:
                request.sendall((msg+MSG_SEPARATOR).encode('utf-8'))
            except socket.error:
                del self.requests[request]

    def send(self, client_id, data):
        msg = ''
        for k,v in data.items():
            msg += k+MSG_SEPARATOR_TAGVALUE+v+MSG_SEPARATOR_TAG
        for request in list(self.requests):
            if client_id == self.requests[request]['client_id']:
                try:
                    request.sendall((msg+MSG_SEPARATOR).encode('utf-8'))
                except socket.error:
                    del self.requests[request]

    def sendRaw(self, client_id, data):
        for request in list(self.requests):
            if client_id == self.requests[request]['client_id']:
                try:
                    request.sendall(data.encode('utf-8'))
                except socket.error:
                    del self.requests[request]

    def disconnect(self, client_id):
        for request in list(self.requests):
            if client_id == self.requests[request]['client_id']:
                self.shutdown_request(request)
                del self.requests[request]
