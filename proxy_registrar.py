#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class PXMLHandler(ContentHandler):

    def __init__(self):
        '''
        Constructor. Inicializamos las variables
        '''
        self.tags = []
        self.list_tags = ['server', 'database', 'log']
        self.dict_attrs = {'server': ['name', 'ip', 'puerto'],
                           'database': ['path', 'passwdpath'],
                           'log': ['path']}

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
    
def proxy_parser_xml(fxml):
    '''
    Función que dado un fichero xml, devuelve una lista de diccionarios
    '''   
    parser = make_parser()
    handxml = PXMLHandler()
    parser.setContentHandler(handxml)
    parser.parse(open(fxml))
    return (handxml.get_tags())

class PHandler(socketserver.DatagramRequestHandler):
    '''
    Handler del Proxy
    '''
    
    datos = proxy_parser_xml(sys.argv[1])
    dbpath = datos[1]['path']
    dbpasswpath = datos[1]['passwdpath']
    logpath = datos[2]['path']
    
    dicdb = {} #Diccionario en el que se van a guardar los usuarios
               #
    def Register(self, data):
        '''
        Funcion para guardar los datos de usuario en un diccionario
        '''
        user = data[0].split(':')[1]
        userip = self.client_address[0]
        userport = data[0].split(' ')[1].split(':')[2]
        userdate = time.time()
        userexp = data[1].split(':')[1][1:]
        print(user, userip, userport, userdate, userexp)

    def handle(self):
    
        DATOS = []
        
        for line in self.rfile:
            DATOS.append(line.decode('utf-8'))
        #Si la petición está mal formada --> 400
        if ('sip:' not in DATOS[0].split(' ')[1] 
            or '@' not in DATOS[0].split(' ')[1] 
            or DATOS[0].split(' ')[2] != 'SIP/2.0\r\n'):
            self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
        else:
            if DATOS[0].split(' ')[0] == 'REGISTER':
                self.Register(DATOS)
            elif DATOS[0].split(' ')[0] == 'INVITE':#IP y Puerto guardados(nombre) con el register
                print('INVITE')
            #elif dcline[0] == 'ACK':
                #os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3])
            elif DATOS[0].split(' ')[0] == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                 
                #401 y 404

            else:
                self.wfile.write(bytes('SIP/2.0 405 Method Not ' +
                                               'Allowed\r\n\r\n', 'utf-8'))

      


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit('Usage: python3 proxy_registrar.py config')
    
    datos = proxy_parser_xml(sys.argv[1])
    username = datos[0]['name']
    if username == '':
        username = 'default'
    proxyip = datos[0]['ip']
    if proxyip == '':
        proxyip = '127.0.0.1'
    proxyport = datos[0]['puerto']
    try:

        serv = socketserver.UDPServer((proxyip, int(proxyport)), PHandler)
        print('Server ' + username + ' listening at port ' + proxyport + '...')
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor proxy")
