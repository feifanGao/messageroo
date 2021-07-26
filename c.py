# coding: utf-8
from socket import *
import sys

# define parameters
serverName = sys.argv[1]  # IP address
serverPort = int(sys.argv[2])  # port number
serverAddr = (serverName, serverPort) # tuple
# create socket with IPv4 and TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# connect server
clientSocket.connect(serverAddr)

# Authentication
# ask for username and password
username = raw_input('Username: ')
password = raw_input('Password: ')
# send username and password
clientSocket.send(username)
clientSocket.send(password)
# receive status
loginStatus = clientSocket.recv(1024)
while True:
    if loginStatus == "locking":
        # block the user for a duration of block_duration seconds
        print 'Your account is blocked due to multiple login failures. Please try again later'
        exit(0)
    elif loginStatus == "locked":
        # block the user for a duration of block_duration seconds
        print 'Invalid Password. Your account has been blocked. Please try again later'
        exit(0)
    elif loginStatus == "successful":
        # display the welcome message
        print 'Welcome to the greatest messaging application ever!'
        break
    elif loginStatus == "failed":
        # give the user opportunity to try again  
        print 'Invalid Password. Please try again'
        # ask for username and password
        password = raw_input('Password: ')
        # send username and password
        clientSocket.send(username)
        clientSocket.send(password)
        # receive status
        loginStatus = clientSocket.recv(1024)

while True:
    data = raw_input('>')
    clientSocket.send(data.strip())
    response = clientSocket.recv(1024)
    if data.startswith("logout"):
        # close socket
        clientSocket.close()
        break
    elif data.startswith("whoelse"):
        if response != "-":
            response = response.split(" ")
            for u in response:
                print('>' + u)
        continue
    elif data.startswith("whoelsesince"):
        if response != "-":
            response = response.split(" ")
            for u in response:
                print('>' + u)
        continue
    continue

exit(0)