#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Clase (y programa principal) para un servidor de eco en UDP simple
'''

import os
import socket
import socketserver
import sys
import uaclient 

class SHandler(socketserver.DatagramRequestHandler):
    '''
    Echo server class
    '''
    def handle(self):
    
        DATOS = []
        DATAXML = uaclient.parser_xml(sys.argv[1])
        PROXYIP = DATAXML[3]['ip']
        PROXYPORT = DATAXML[3]['puerto'] 

        for line in self.rfile:
            DATOS.append(line.decode('utf-8'))
        
        okinv = () 
                 #añadir el sdp a 100, 180, 200

        if DATOS[0].split(' ')[0] == 'INVITE':
            print(DATAXML)
            print(DATOS)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((PROXYIP, int(PROXYPORT)))
                my_socket.send(bytes('SIP/2.0 100 Trying\r\n\r\n' +
                     'SIP/2.0 180 Ringing\r\n\r\n' + 'SIP/2.0 200 OK\r\n\r\n' +
                     'Content-Type: application/sdp\r\n\r\n' + 'v=0\r\n' +
                     'o=' + DATAXML[0]['username'] + ' ' + DATAXML[1]['ip'] +
                     '\r\n' + 's=mysession\r\n' + 't=0\r\n' + 'm=audio ' +
                     str(DATAXML[2]['puerto']) + ' RTP\r\n', 'utf-8'))
            
        
        
    
                    #os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' +
                     #         sys.argv[3])


                #401 y 404


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('Usage: python3 uaserver.py config')
    DATAXML = uaclient.parser_xml(sys.argv[1])    
    MSERVER = DATAXML[1]['ip']
    if MSERVER == '':
        MSERVER = '127.0.0.1'
    MSPORT = DATAXML[1]['puerto']
    try:
        serv = socketserver.UDPServer((MSERVER, int(MSPORT)), SHandler)
        print('Listening...')
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Finalizado uaserver')
