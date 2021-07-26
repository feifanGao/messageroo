# coding: utf-8
import socket
import sys
import threading
import time

condition = threading.Condition()

# Authentication
class User:
    def __init__(self, username, password, lockDuration, timeoutPeriod):
        self.lastLoginAt = 0

        self.username = username
        self.password = password
        self.nChances = 3
        
        self.isLocked = False
        self.isLockedSince = 0
        self.lockDuration = lockDuration

        self.isOnline = False
        self.inactiveSince = int(time.time())
        self.timeoutPeriod = timeoutPeriod

        self.blocks = set()

    '''
    def __str__(self):
        string = self.username
        return string
    '''

userList = []

def readFile(lockDuration, timeoutPeriod):
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
            user = User(credential[0], credential[1], lockDuration, timeoutPeriod)
            userList.append(user)

def authenticate(un, pw):
    for u in userList:
        if u.username == un:
            if u.isOnline == True:
                return "already"
            if u.isLocked == True:
                return "locking"
            if u.password == pw:
                u.nChances = 3
                u.isLockedSince = 0
                u.isOnline = True
                u.inactiveSince= int(time.time())
                u.lastLoginAt = int(time.time())
                return "successful"
            else:
                u.nChances -= 1
                if u.nChances <= 0:
                    u.isLocked = True
                    u.isLockedSince = int(time.time())
                    return "locked"
                return "failed"
    # no matching username
    return "failed"

def getUser(un):
    for u in userList:
        if u.username == un:
            return u
    return null

# define parameters
serverName = "localhost"
serverPort = int(sys.argv[1])
lockDuration = int(sys.argv[2])
timeoutPeriod = int(sys.argv[3])
readFile(lockDuration, timeoutPeriod)
serverAddr = (serverName, serverPort) # tuple
# create socket with IPv4 and TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind address
serverSocket.bind(serverAddr)
print("The server is ready to receive")
# listen for connection
serverSocket.listen(10)

def receive(clientSocket, clientAddr):
    print("Connection from %s:%s" % clientAddr)
    # receive username and password
    username = clientSocket.recv(1024)
    password = clientSocket.recv(1024)
    # logging in
    while True:
        # authenticate client
        loginStatus = authenticate(username, password)
        # send status
        clientSocket.send(loginStatus)
        if loginStatus == "successful":
            # locate the user
            user = getUser(username)
        elif loginStatus == "failed":
            # receive username and password
            username = clientSocket.recv(1024)
            password = clientSocket.recv(1024)
            continue
        break
    # messaging
    while True:
        line = clientSocket.recv(1024)
        data = line.split(" ")
        command = data[0]
        response = "-"
        # time.sleep(1)
        if command == "logout":
            response = "logout"
            user.isOnline = False
            # send response
            clientSocket.send(response)
            clientSocket.close()
            print('Connection from %s:%s closed.' % clientAddr)
        elif command == "whoelse":
            whoelseList = []
            for u in userList:
                if u is not user and u.isOnline == True:
                    whoelseList.append(u.username)
            if whoelseList != []:
                response = " ".join(whoelseList)
            clientSocket.send(response)
            continue
        elif command == "whoelsesince" and len(data) >= 2:
            whoelsesinceList = []
            period = int(data[1])
            now = time.time()
            for u in userList:
                if u is not user and u.lastLoginAt + period >= now:
                    whoelsesinceList.append(u.username)
            if whoelsesinceList != []:
                response = " ".join(whoelsesinceList)
            clientSocket.send(response)
            continue
        continue

# accept the connection
clientSocket, clientAddr = serverSocket.accept()
# create new thread to handle the connection
newReceiveThread = threading.Thread(target=receive, args=(clientSocket, clientAddr))
newSendThread = threading.Thread(target=send, args=(clientSocket, clientAddr))
newThread.start()