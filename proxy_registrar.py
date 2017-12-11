#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import socketserver
import sys
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    sipdic = {}
    
    def register2json(self):
        json.dump(self.sipdic, open('registered.json', 'w'))


    def handle(self):
        print('IP cliente: ' + self.client_address[0] + '\t'
         + 'Puerto cliente: ' + str(self.client_address[1]))
        listdel = []
        for line in self.rfile:
            decodlin = line.decode('utf-8')
            print(decodlin)
            if not line:
                continue
                
            elif decodlin.split(' ')[0] == 'REGISTER':
                sipusr = decodlin.split(' ')[1][decodlin.split(' ')[1].find(':') + 1 :] 
                self.sipdic[sipusr] = [self.client_address[0], 0]
                self.register2json()

            elif decodlin.split(' ')[0] == 'Expires:':
                expt = float(decodlin.split(' ')[1]) + time.time()
                self.sipdic[sipusr][1] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expt))
                for user in self.sipdic:
                    if self.sipdic[user][1] <= time.strftime('%Y-%m-%d %H:%M:%S',
                     time.gmtime(time.time())):
                        listdel.append(user)
                        print('Tiempo expirado')
                    else:
                        print('Tiempo no expirado')
                
                for user in listdel:
                    del self.sipdic[user]
                    print('Diccionario:', self.sipdic)
                self.register2json()
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
            else:
                pass
   
if __name__ == "__main__":

    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
