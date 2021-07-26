from socket import *
import pickle
import sys
import threading

class User:
    def __init__(self, un, pw, n):
        self.username = un
        self.password = pw
        self.nChances = n

userList = []

with open('credentials.txt', 'r') as f:
    i = 0
    while 1:
        line = f.readline()
        i += 1
        if line == "":
            break
        # omit the new line character
        # split by space
        credential = line[:-2].split(" ", 2)
        user = User(credential[0], credential[1], 3)
        userList.append(user)


def authenticate(un, pw):
    for u in userList:
        if u.username == un:
            if u.nChances <= 0:
                return "blocking"
            if u.password == pw:
                # u.isOnline = True
                # print(userList)
                u.nChances = 3
                return "successful"
            else:
                u.nChances -= 1
                if u.nChances <= 0:
                    return "blocked"
                return "failed"
    return "failed"


def comm(currPort):
    global serverName
    global TIMEOUT_INTERVAL
    global allClients
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, currPort))
    serverSocket.listen(0)
    print(currPort)
    connectionSocket, addr = serverSocket.accept()
    allClients[currPort] = connectionSocket
    auth = False
    #receive data
    while True:
        try:
            receivedMessage = connectionSocket.recv(2048)
        except timeout:
            print("timeout")
            returnMessage = "Your connection is timeout!"
            connectionSocket.send(returnMessage.encode())
            connectionSocket.close()
            return
        if (not auth):
            mes = pickle.loads(receivedMessage)
            if (authenticate(mes[0], mes[1]) == "successful"):
                print("ok")
                auth = True
                returnMessage = "Welcome to the greatest messaging application ever!"
                connectionSocket.send(returnMessage.encode())
                connectionSocket.settimeout(TIMEOUT_INTERVAL)
            else:
                print("not ok")
                returnMessage = "Invalid Password. Please try again"
                connectionSocket.send(returnMessage.encode())
        else:
            print(receivedMessage.decode())



def command():
    global allClients
    while True:
        command = input()
        if (command[0] == "broadcast"):
            #print(command[2:])
            for socket in list(allClients.values()):
                socket.send(command[2:].encode())
        if (command[0] == "message"):
            argv = command.split(" ")
            socket = allClients[int(argv[1])]
            socket.send(argv[2].encode())

serverName = 'localhost'
serverPort = 4000
currPort = 4001
TIMEOUT_INTERVAL = 60
auth = False
allClients = dict()

commandThreading = threading.Thread(target=command)
commandThreading.start()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(0)
#sys.exit()
while True:
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send(str(currPort).encode())
    connectionSocket.close()
    t1 = threading.Thread(target=comm, args=(currPort,))
    t1.start()
    currPort += 1