#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple HTTP Server
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket
import random


# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('localhost', 13579))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an infinite loop)

sumandos = 0 #si no lo inicializo no entra al if
try:
    while True:
        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'Request received:'
        solicitud = recvSocket.recv(2048)
        print 'Answering back...'
        try:
            numero = int(solicitud.split()[1][1:])
        except KeyError:
            continue

        if (sumandos == 0):
            sumandos = numero;
            resultado = "Dame otro numero, por favor";
        else:
            suma = numero + sumandos;
            resultado = "El resultado de la suma es:" + str(numero) + "+" + str(sumandos) + "=" + str(suma);
            sumandos = 0; 

        recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                        "<html><body><h1>" +
                        	resultado + "</p>" + "</h1></body></html>" + "\r\n")
        recvSocket.close()
except KeyboardInterrupt:
	print "Closing binded socket"
	mySocket.close()

