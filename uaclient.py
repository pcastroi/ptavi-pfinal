#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Programa User Agent Client
'''

import hashlib
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


def ClientRegister(data):
    '''
    Funcion para Register: Asumimos que el valor de option es un Expires correcto
    Devuelve el mensaje que se envía para reusarlo en la autorización
    '''
    try:
        int(sys.argv[3])
    except ValueError:
        sys.exit('Usage: python3 uaclient.py config method option')
        CLog('Finishing.', data[4]['path'])
            
    msend = ('REGISTER' + ' sip:' + data[0]['username'] + ':' + data[1]['puerto'] +
             ' SIP/2.0\r\n' + 'Expires: ' + sys.argv[3] + '\r\n')
    CLog('Sent to ' + data[3]['ip'] + ':' + data[3]['puerto'] + ': ' + msend, data[4]['path'])
    my_socket.send(bytes(msend, 'utf-8') + b'\r\n')
    return msend
            
def ClientInvite(data, receiver):
    '''
    Funcion para Invite:
    '''
    if '@' not in receiver or '.' not in receiver:
        CLog('Finishing.', data[4]['path'])
        sys.exit('Usage: python3 uaclient.py config method option')
    else:
        msend = ('INVITE' + ' sip:' + receiver + ' SIP/2.0\r\n' +
                 'Content-Type: application/sdp\r\n\r\n' + 'v=0\r\n' +
                 'o=' + data[0]['username'] + ' ' + data[1]['ip'] +
                 '\r\n' + 's=mysession\r\n' + 't=0\r\n' + 'm=audio ' +
                  data[2]['puerto'] + ' RTP\r\n')
        CLog('Sent to ' + data[3]['ip'] + ':' + data[3]['puerto'] + ': ' + msend, data[4]['path'])
        my_socket.send(bytes(msend, 'utf-8') + b'\r\n')
                
  
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
    USER = DATAXML[0]['username']
    PASSWORD = DATAXML[0]['passwd']
    RTPPORT = DATAXML[2]['puerto']
    LOGPATH = DATAXML[4]['path']
    PROXYIP = DATAXML[3]['ip']
    PROXYPORT = DATAXML[3]['puerto']
    SERVERIP = DATAXML[1]['ip']
    if SERVERIP == '':
        SERVERIP = '127.0.0.1'
    SERVERPORT = DATAXML[1]['puerto']
    DATALIST = [USER, PASSWORD, SERVERIP, SERVERPORT]
    CLog('Starting...', LOGPATH)
        
    #Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((PROXYIP, int(PROXYPORT)))
        
        if METHOD == 'REGISTER':
            msend = ClientRegister(DATAXML)
        elif METHOD == 'INVITE':
            ClientInvite(DATAXML, OPTION)
        elif METHOD == 'BYE':    
            if '@' not in OPTION or '.com' not in OPTION:
                CLog('Finishing.', LOGPATH)
                sys.exit('Usage: python3 uaclient.py config method option')
            else:
                my_socket.send(bytes('BYE sip:' + OPTION + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
                CLog('Sent to ' + PROXYIP + ':' + PROXYPORT +
                     ': ' + 'BYE sip:' + OPTION + ' SIP/2.0\r\n', LOGPATH)
                
        #Excepción si el método introducido no es válido 
        else:
            CLog('Finishing.', LOGPATH)
            sys.exit('Usage: python3 uaclient.py config method option')
            
        try:
            data = my_socket.recv(1024).decode('utf-8')
            print(data)
            dataline = data.split('\r\n')
            CLog('Received from ' + PROXYIP + ':' + PROXYPORT + 
                 ': ' + data, LOGPATH)
            #Autorización del cliente
            if dataline[0].split(' ')[1] == '401':
                nonce = dataline[1].split('=')[1][1:-1]
                h = hashlib.sha1(bytes(PASSWORD, 'utf-8'))
                h.update(bytes(nonce, 'utf-8'))
                msend = (msend + '\r\n' + 'Authorization: Digest response="' +
                         h.hexdigest() + '"\r\n\r\n')
                my_socket.send(bytes(msend , 'utf-8') + b'\r\n')
                CLog('Sent to ' + PROXYIP + ':' + PROXYPORT + ': ' + msend, LOGPATH)
                #Esperamos a recibir el Ok
                data2 = my_socket.recv(1024).decode('utf-8')
                dataline2 = data2.split('\r\n')
                CLog('Received from ' + PROXYIP + ':' + PROXYPORT + 
                     ': ' + data2, LOGPATH)
                if dataline2[0].split(' ')[1] == '200':
                    print('Registrado correctamente')
                else:
                    sys.exit('no se ha recibido el ok')
            #Envio del ACK
            elif dataline[0].split(' ')[1] == '100':
                my_socket.send(bytes('ACK sip:' + OPTION + 
                                     ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
                CLog('Sent to ' + PROXYIP + ':' + PROXYPORT +
                     ': ' + 'ACK sip:' + OPTION + ' SIP/2.0\r\n', LOGPATH)
        #Este error deberia salir al intentar conectar un ua con el servidor proxy apagado.
        except ConnectionRefusedError:
            CLog('Error: No server listening at ' + PROXYIP + ' port ' + PROXYPORT, LOGPATH)
            CLog('Finishing.', LOGPATH)
            sys.exit('Connection Refused Error')
        #Error cuando no responde el proxy
        except IndexError:
            sys.exit('No response')
            
        CLog('Finishing.', LOGPATH)
