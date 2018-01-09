#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time

class XMLHandler(ContentHandler):

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
        
def parser_xml(fxml):
    '''
    Función que dado un fichero xml, devuelve una lista de diccionarios
    '''   
    parser = make_parser()
    handxml = XMLHandler()
    parser.setContentHandler(handxml)
    parser.parse(open(fxml))
    return (handxml.get_tags())

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit('Usage: python3 proxy_registrar.py config')

    DATAXML = parser_xml(sys.argv[1])
    print(DATAXML)
    
    #Variables que vamos a usar
    PNAME = DATAXML[0]['name']
    if NAME == '':
        NAME = 'default'
    PSERVER = DATAXML[0]['ip']
    if MSERVER == '':
        MSERVER = '127.0.0.1'
    PSPORT = DATAXML[0]['puerto']
    DBP = DATAXML[1]['path']
    DBPSWDP = DATAXML[1]['passwdpath']
    LOGP = DATAXML[2]['path']
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor proxy")
