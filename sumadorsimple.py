#!/usr/bin/python3

#Sumador version 2: Ejercicio 14.5, se ejecuta pasandole en el navegador: localhost:1234/numero1 -->
#y nos imprime un mensaje diciendo que numero le hemos enviado y pidiendo otro. Luego volvemos a poner
#localhost:1234/numero2 y nos dice el numero que le habiamos pasado (numero1) y el que le hemos pasado
#ahora, ademas nos devuelve la suma.
#En caso de introducir algo que no sea un numero para que se pueda sumar debemos imprimir un mensaje de
#error guardando el numero1 que ya teniamos
"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.

Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

sumandos = 0

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept() #address es una lista con mi IP en pos[0] y puerto del servidor en pos[1]
        print('Request received:')
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")   #son bytes pasados a utf-8
        print(peticion)

        try:
            #necesito dos numeros para sumarlos, primero introduzco uno y luego el otro
            #introduzco el primero
            numero = peticion.split()[1][1:]
            print (numero)
            if numero == "favicon.ico":
                recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" + "Paso de ti\r\n", 'utf-8')) #si la peticion es favicon.ico paso de ella y sigo
                recvSocket.close()
                continue
            print('Answering back...')

            #para saber si es el primero puedo guardarlo en una varia que si esta vacia me diga que es el primer numero
            #y si esta llena es que es el segundo y hay que sumarlo
            if (sumandos == 0):             #si mi variable sumandos es cero es que es el primer numero
                sumandos = numero           #guardo mi numero en una variable sumandos, asi luego vera que sumandos no es cero
                resultado = "Me has enviado un " + str(sumandos) + " .Dame otro mas"
            else:                           #si mi variable no es cero es que es el segundo numero que meto
                sumando2 = numero
                suma = int(sumandos) + int(sumando2)
                resultado = "Me habias enviado un " + str(sumandos) + " . Ahora un " + str(sumando2) + ". La suma es: " + str(suma)
                sumandos = 0                #debo inicializar a cero de nuevo para que vuelva a iniciarse el proceso

            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body><h1>" + resultado + "</h1></body></html>" +
                            "\r\n", 'utf-8'))
            recvSocket.close()
        except ValueError:
            resultado = resultado = "Me habias enviado un " + str(sumandos) + " . Ahora un " + str(sumando2) + ". No me vale, introduce un numero"
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body><h1>" + resultado + "</h1></body></html>" +
                            "\r\n", 'utf-8'))
            recvSocket.close()
except KeyboardInterrupt:
    print("Closing binded socket")
    mySocket.close()
