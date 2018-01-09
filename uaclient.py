#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Programa User Agent Client
'''

import os
import socket
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

#Creamos una clase para leer el contenido del fichero de configuración xml
class XMLHandler(ContentHandler):

    def __init__(self):
        '''
        Constructor. Inicializamos las variables
        '''
        self.tags = []
        self.list_tags = ['account', 'uaserver', 'rtpaudio', 
                          'regproxy','log', 'audio']
        self.dict_attrs = {'account': ['username', 'passwd'],
                           'uaserver': ['ip', 'puerto'],
                           'rtpaudio': ['puerto'],
                           'regproxy': ['ip', 'puerto'],
                           'log': ['path'],
                           'audio': ['path']}

    def startElement(self, name, attrs):
        '''
        Método de inicio
        '''
       
        if name in self.list_tags:
            diccionario = {}
            diccionario['tag'] = name
            for atributo in self.dict_attrs[name]:
                diccionario[atributo] = attrs.get(atributo, '')
            self.tags.append(diccionario)

    def get_tags(self):
        '''
        Devuelve la lista
        '''
        return self.tags
        
def parser_xml(fxml):
    '''
    Función que dado un fichero xml, devuelve una lista de diccionarios
    '''   
    parser = make_parser()
    handxml = XMLHandler()
    parser.setContentHandler(handxml)
    parser.parse(open(fxml))
    return (handxml.get_tags())

def CLog(data, log):
    '''
    Función que crea el log, no está bien aún.
    '''
    timenow = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))
    flog = open(log, 'a')
    data = data.replace('\r\n',' ')
    flog.write(timenow + ' ' + data + '\r\n')
    flog.close()
    
if __name__ == '__main__':
    '''
    Programa principal
    '''   
    #Compruebo los argumentos de entrada(nº de parámetros y si son correctos o no)

    if len(sys.argv) != 4:
        sys.exit('Usage: python3 uaclient.py config method option')
    DATAXML = parser_xml(sys.argv[1])
    
    #Variables que vamos a usar
    METHOD = sys.argv[2]
    OPTION = sys.argv[3]
    MLOGIN = DATAXML[0]['username']
    RTPPORT = DATAXML[2]['puerto']
    PLOG = DATAXML[4]['path']
    MPROXY = DATAXML[3]['ip']
    MPPORT = DATAXML[3]['puerto']
    CLog('Starting...', PLOG)
        
    #Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((MPROXY, int(MPPORT)))
        
        #Asumimos que el valor de option es un Expires correcto
        if METHOD == 'REGISTER': 
            try:
                int(OPTION)
            except ValueError:
                sys.exit('Usage: python3 uaclient.py config method option')
                CLog('Finishing.', PLOG)
                    
            msend = (METHOD + ' sip:' + MLOGIN + ':' + MPPORT +
                     ' SIP/2.0\r\n' + 'Expires: ' + OPTION + '\r\n')
            print(msend)
            CLog('Sent to ' + MPROXY + ':' + MPPORT + ': ' + msend, PLOG)
            my_socket.send(bytes(msend, 'utf-8') + b'\r\n')
            
        elif METHOD == 'INVITE':
            if '@' not in OPTION or '.' not in OPTION:
                sys.exit('Usage: python3 uaclient.py config method option')
                CLog('Finishing.', PLOG)
            else:
                msend = (METHOD + ' sip:' + OPTION + ' SIP/2.0\r\n' +
                         'Content-Type: application/sdp\r\n\r\n' + 'v=0\r\n' +
                         'o=' + MLOGIN + ' ' + MPROXY + '\r\n' + 's=mysession\r\n' +
                         't=0\r\n' + 'm=audio ' + RTPPORT + ' RTP\r\n')
                print(msend)
                CLog('Sent to ' + MPROXY + ':' + MPPORT + ': ' + msend, PLOG)
                my_socket.send(bytes(msend, 'utf-8') + b'\r\n')
                
        elif METHOD == 'BYE':    
            if '@' not in OPTION or '.com' not in OPTION:
                sys.exit('Usage: python3 uaclient.py config method option')
                CLog('Finishing.', PLOG)
            else:
                my_socket.send(bytes('BYE sip:' + OPTION + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
                CLog('Sent to ' + MPROXY + ':' + MPPORT + ': ' + 'BYE sip:' + OPTION + ' SIP/2.0\r\n', PLOG)
        else:
            CLog('Finishing.', PLOG)
            sys.exit('Usage: python3 uaclient.py config method option')
            
        try:   
            data = my_socket.recv(1024)
            print(data.decode('utf-8'))
            CLog(data.decode('utf-8'), PLOG)
        #Este error deberia salir al interntar conectar un ua con el servidor proxy apagado.
        except ConnectionRefusedError:
            CLog('Error: No server listening at ' + MPROXY + ' port ' + MPPORT, PLOG)
            CLog('Finishing.', PLOG)
            sys.exit()
            
        CLog('Received from ', PLOG)
        #Autorización del cliente
        if data.decode('utf-8').split()[1] == '401':
            msend = msend + '\r\n' + 'Authorization: Digest response="123123212312321212123"'
            my_socket.send(bytes(msend , 'utf-8') + b'\r\n')
            CLog('Sent to ' + MPROXY + ':' + MPPORT + ': ' + msend, PLOG)
        #Envio del ACK
        if data.decode('utf-8').split()[1] == '100':
            my_socket.send(bytes('ACK sip:' + OPTION + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
            CLog('Sent to ' + MPROXY + ':' + MPPORT + ': ' + 'ACK sip:' + OPTION + ' SIP/2.0\r\n', PLOG)
            
        CLog('Finishing.', PLOG)
