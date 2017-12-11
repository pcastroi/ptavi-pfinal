#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa User Agent Client
"""

import socket
import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


#Creamos una clase para leer el contenido del fichero de configuración xml
class XMLHandler(ContentHandler):

    def __init__(self):
        """
        Constructor. Inicializamos las variables
        """
        self.list_tags = []
        self.tags = {'account': ['username', 'passwd'],
                     'uaserver': ['ip', 'puerto'],
                     'rtpaudio': 'puerto',
                     'regproxy': ['ip', 'puerto'],
                     'log': 'path',
                     'audio': 'path'}

    def startElement(self, name, attrs):
        """
        Método de inicio
        """
        print("a")
        diccionario = {}
        if name in self.tags:
            print("B")
            diccionario['tag'] = name
            for elem in self.tags[name]:
                diccionario[elem] = attrs.get(elem, "")
            self.list_tags.append(diccionario)

    def get_tags(self):
        """
        Devuelve la lista
        """
        return self.list_tags
        
    def __str__(self):
        """
        Devuelve una cadena de texto con todas las etiquetas y atributos
        """
        listcad = []
        for dic in self.list_tags:
            listcad.append(dic['tag'])
            for atribs in dic:
                if atribs != 'tag' and dic[atribs]:
                    listcad.append('\t' + atribs + '=' + dic[atribs] + '\t')
            listcad.append('\n')
        return(''.join(listcad))

if __name__ == '__main__':
    # Compruebo los argumentos de entrada
    if len(sys.argv) != 4:
        sys.exit("Usage: python uaclient.py config method option")

    # Argumentos que me pasan como parámetros
    CONFIG = sys.argv[1]
    METHOD = sys.argv[2]
    OPTION = sys.argv[3]


    parser = make_parser()
    listxml = XMLHandler()
    parser.setContentHandler(listxml)
    print(CONFIG)
    parser.parse(open(CONFIG))
    print(listxml.__str__())
    




# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto

#with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

#    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    my_socket.connect((MSERVER, int(MPORT)))

#    Msend = 'sip:' + MLOGIN + '@' + MSERVER + ' SIP/2.0\r\n'
#    my_socket.send(bytes(METHOD + ' ' + Msend, 'utf-8') + b'\r\n')
#    data = my_socket.recv(1024)
#    print(data.decode('utf-8'))

#    if data.decode('utf-8').split()[1] == "100":
#        my_socket.send(bytes("ACK" + ' ' + Msend, 'utf-8') + b'\r\n')
#    print("Conection finished.")
