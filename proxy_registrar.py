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
        
        
        
        
def DicReg(data, dic):
    '''
    Funcion para guardar los datos de usuario en un diccionario
    '''
    regline = data.readlines()[0].split(' ')[1]
    user = regline.split(':')[1]
    userip = self.client_address[0]
    userport = regline.split(':')[2]
    userdate = time.time()
    userexp = data.readlines()[1].split(' ')[1]
    '''
    información relativa a un usuario, en particular, su dirección, su
    IP, su puerto, la fecha del registro (en segundos desde el 1 de enero de 1970) y el
    tiempo de expiración (en segundos).
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    

class PHandler(socketserver.DatagramRequestHandler):
    '''
    Handler del Proxy
    '''
    dicdb = {}
    def handle(self):
        while 1:
            okinv = ('SIP/2.0 100 Trying\r\n\r\n' +
                     'SIP/2.0 180 Ringing\r\n\r\n' + 
                     'SIP/2.0 200 OK\r\n\r\n')
            line = self.rfile.read()
            dcline = line.decode('utf-8').split(' ')
            lines = line.decode('utf-8').split('\r\n')
            print(line.decode('utf-8'))
            if str(dcline[0]) != '':
                if ('sip:' not in lines[0].split(' ')[1] or '@' not in lines[0].split(' ')[1] or lines[0].split(' ')[2] != 'SIP/2.0\r\n\r\n'):
                    self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

                else:
                    print('NO ENVIA BAD REQUEST')
                    if dcline[0] == 'REGISTER':
                        SaveReg(line, self.dicdb)
                        
                    elif dcline[0] == 'INVITE':#IP y Puerto guardados(nombre) con el register
                        print('INVITE')
                    #elif dcline[0] == 'ACK':
                        #os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3])

                    elif dcline[0] == 'BYE':
                        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                        
                    #401 y 404

                    else:
                        self.wfile.write(bytes('SIP/2.0 405 Method Not ' +
                                               'Allowed\r\n\r\n', 'utf-8'))

            if not line:
                break

      
def proxy_parser_xml(fxml):
    '''
    Función que dado un fichero xml, devuelve una lista de diccionarios
    '''   
    parser = make_parser()
    handxml = PXMLHandler()
    parser.setContentHandler(handxml)
    parser.parse(open(fxml))
    return (handxml.get_tags())

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit('Usage: python3 proxy_registrar.py config')

    DATAXML = proxy_parser_xml(sys.argv[1])
    
    #Variables que vamos a usar
    PNAME = DATAXML[0]['name']
    if PNAME == '':
        PNAME = 'default'
    PSERVER = DATAXML[0]['ip']
    if PSERVER == '':
        PSERVER = '127.0.0.1'
    PSPORT = DATAXML[0]['puerto']
    DBP = DATAXML[1]['path']
    DBPSWDP = DATAXML[1]['passwdpath']
    LOGP = DATAXML[2]['path']
    try:
        print('Server ' + PNAME + ' listening at port ' + PSPORT + '...')
        serv = socketserver.UDPServer((PSERVER, int(PSPORT)), PHandler)
        serv.serve_forever()
        
    except KeyboardInterrupt:
        print("Finalizado servidor proxy")
