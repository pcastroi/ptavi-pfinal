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
                     'rtpaudio': ['puerto'],
                     'regproxy': ['ip', 'puerto'],
                     'log': ['path'],
                     'audio': ['path']}

    def startElement(self, name, attrs):
        """
        Método de inicio
        """
        diccionario = {}
        if name in self.tags:
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

    # Argumentos que me pasan como parámetros
    CONFIG = sys.argv[1]
    METHOD = sys.argv[2]
    OPTION = sys.argv[3]


    parser = make_parser()
    listxml = XMLHandler()
    parser.setContentHandler(listxml)
    parser.parse(open(CONFIG))
    print(listxml.get_tags())
    MLOGIN = listxml.get_tags()[0]['username']
    MSERVER = listxml.get_tags()[1]['ip']
    MPORT = listxml.get_tags()[1]['puerto']
    print(MLOGIN)
    print(MSERVER)
    print(MPORT)

        
#Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((MSERVER, int(MPORT)))
    # Compruebo los argumentos de entrada(nº de parámetros y si son correctos o no)
    if len(sys.argv) != 4
        sys.exit("Usage: python3 uaclient.py config method option")
    if METHOD == "REGISTER": #Asumimos que el valor de option es un Expires correcto
        try:
            int(OPTION)
        except ValueError:
            sys.exit("Usage: python3 uaclient.py config method option")
        
        msend = METHOD + ' sip:' + MLOGIN + ':' + MSERVER + ' SIP/2.0\r\n' + "Expires: " + OPTION
        my_socket.send(bytes(msend, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
        if  
            
            
            
            
    elif METHOD == "INVITE":
        if '@' not in OPTION or '.com' not in OPTION:
            sys.exit("Usage: python3 uaclient.py config method option")
        else:
        
    elif METHOD == "BYE":    
        if '@' not in OPTION or '.com' not in OPTION:
            sys.exit("Usage: python3 uaclient.py config method option")
        else:
        
    else:
        sys.exit("Usage: python3 uaclient.py config method option")
        


    Msend = 'sip:' + MLOGIN + '@' + MSERVER + ' SIP/2.0\r\n'
    my_socket.send(bytes(METHOD + ' ' + Msend, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))



#Añadir la autenticación del register
    if data.decode('utf-8').split()[1] == "100":
        my_socket.send(bytes("ACK" + ' ' + Msend, 'utf-8') + b'\r\n')
    print("Conection finished.")
