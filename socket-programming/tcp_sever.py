from socket import *

serverSocket = socket(AF_INET,SOCK_STREAM)

address = ("127.0.0.1",4980)

serverSocket.bind(address)

serverSocket.listen()
print("Server is ready")

while True:

    (newSocket,clientAddress) = serverSocket.accept()
    print(clientAddress)
    
    byteAnswer = newSocket.recv(2048)

    AnswerStr = byteAnswer.decode()

    upperAns = AnswerStr.upper()

    strToByte = upperAns.encode()

    newSocket.send(strToByte)

    newSocket.close()