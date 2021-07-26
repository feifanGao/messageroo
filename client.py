from socket import *
import pickle
import time
import sys
import threading

##t1.setDaemon(True)##
serverName = sys.argv[1]
serverPort = int(sys.argv[2]) 
auth = False

def receiveFunction():
    global TCP_Socket
    global auth
    while True:
        receivedMessage = TCP_Socket.recv(2048)
        receivedMessage = receivedMessage.decode()
        print(receivedMessage)
        if ('Welcome' in receivedMessage):
            auth = True
        if ('timeout' in receivedMessage):
            return

# establish connection
TCP_Socket2 = socket(AF_INET, SOCK_STREAM)
TCP_Socket2.connect((serverName, serverPort))
receivedMessage = TCP_Socket2.recv(2048)
receivedMessage = receivedMessage.decode()

currPort = int(receivedMessage)
print(currPort)
TCP_Socket2.close()
time.sleep(1)

# recv data
TCP_Socket = socket(AF_INET, SOCK_STREAM)
TCP_Socket.connect((serverName, currPort))
t1 = threading.Thread(target=receiveFunction)
t1.start()

# command
while True:
    time.sleep(1)
    if (not auth):
        # get auth information
        authInfo = []
        authInfo.append(input("Username: "))
        authInfo.append(input("Password: "))
        TCP_Socket.send(pickle.dumps(authInfo))
    else:
        mes = input()
        TCP_Socket.send(mes.encode())