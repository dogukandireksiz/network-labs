from socket import *

serverAddress = ("127.0.0.1", 12000)

clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(5)

sentence = input(str())

sentenceTobytes = sentence.encode()
print(clientSocket.getsockname())
clientSocket.sendto(sentenceTobytes,serverAddress)
print(clientSocket.getsockname())

try:
    (answer, _ ) = clientSocket.recvfrom(2048)

    answerTostring = answer.decode()

    print(answerTostring)
except TimeoutError:
    print("Server is not responding")    

clientSocket.close()