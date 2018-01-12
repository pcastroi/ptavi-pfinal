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
            
        if DATOS[0].split(' ')[0] == 'INVITE':
            msend = ('SIP/2.0 100 Trying\r\n\r\n' +
                    'SIP/2.0 180 Ringing\r\n\r\n' + 'SIP/2.0 200 OK\r\n\r\n' +
                    'Content-Type: application/sdp\r\n\r\n' + 'v=0\r\n' +
                    'o=' + DATAXML[0]['username'] + ' ' + DATAXML[1]['ip'] +
                    '\r\n' + 's=mysession\r\n' + 't=0\r\n' + 'm=audio ' +
                    str(DATAXML[2]['puerto']) + ' RTP\r\n')
            self.wfile.write(bytes(msend, 'utf-8'))
            #log
        elif DATOS[0].split(' ')[0] == 'ACK':
            os.system('./mp32rtp -i ' + DATAXML[1]['ip'] + '-p ' + DATAXML[2]['puerto'] +
                      ' < ' + DATAXML[5]['path'])
        elif DATOS[0].split(' ')[0] == 'BYE':
            msend = 'SIP/2.0 200 OK\r\n\r\n'   
            self.wfile.write(bytes(msend, 'utf-8'))
        print(DATOS)

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
