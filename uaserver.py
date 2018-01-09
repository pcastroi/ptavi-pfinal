#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Clase (y programa principal) para un servidor de eco en UDP simple
'''

import os
import socketserver
import sys
import uaclient 

class SHandler(socketserver.DatagramRequestHandler):
    '''
    Echo server class
    '''
    def handle(self):#Falta el sdp cuando mando 200 ok
        while 1:
            okinv = ('SIP/2.0 100 Trying\r\n\r\n' +
                     'SIP/2.0 180 Ringing\r\n\r\n' + 'SIP/2.0 200 OK\r\n\r\n')
            line = self.rfile.read()
            dcline = line.decode('utf-8').split(' ')
            print(line.decode('utf-8'))
            if str(dcline[0]) != '':
                if ('sip:' not in dcline[1] or '@' not in dcline[1] or
                   dcline[2] != 'SIP/2.0\r\n\r\n'):
                    self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

                else:
                    if dcline[0] == 'INVITE':
                        self.wfile.write(bytes(okinv, 'utf-8'))

                    elif dcline[0] == 'ACK':
                        os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' +
                                  sys.argv[3])

                    elif dcline[0] == 'BYE':
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                        
                    #401 y 404

                    else:
                        self.wfile.write(bytes('SIP/2.0 405 Method Not ' +
                                               'Allowed\r\n\r\n', 'utf-8'))

            if not line:
                break

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('Usage: python3 uaserver.py config')

    DATAXML = uaclient.parser_xml(sys.argv[1])
    MSERVER = DATAXML[1]['ip']
    if MSERVER == '':
        MSERVER = '127.0.0.1'
    MSPORT = DATAXML[1]['puerto']
    print(DATAXML)
    serv = socketserver.UDPServer((MSERVER, int(MSPORT)), SHandler)
    print('Listening...')
    serv.serve_forever()
