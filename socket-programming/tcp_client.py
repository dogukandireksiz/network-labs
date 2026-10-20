from socket import *

serverAddress = ("127.0.0.1",4980)

clientSocket = socket(AF_INET,SOCK_STREAM)

print(clientSocket.getsockname())
clientSocket.connect(serverAddress)
print(clientSocket.getsockname())

print("client connected to server")

sentence = input(str("give a sentence: "))

bytSentence = sentence.encode()

clientSocket.send(bytSentence)

byteAns = clientSocket.recv(2048)

strAns = byteAns.decode()

print(strAns)

clientSocket.close()


