# 1. socket modülünü içe aktar
# 2. UDP socket oluştur (AF_INET, SOCK_DGRAM)
# 3. bind: ('', 12000)
# 4. "server hazır" yazdır
# 5. sonsuz döngü:
#    5a. recvfrom ile veri ve adresi al
#    5b. bytes'ı str'ye çevir
#    5c. büyük harfe çevir
#    5d. str'yi tekrar bytes'a çevir
#    5e. sendto ile gelen adrese geri yolla


from socket import *

#create UDP socket
serverSocket = socket(AF_INET,SOCK_DGRAM)
address = ("127.0.0.1",12000)
serverSocket.bind(address)
print("Server is ready")

while True:
    (byteS , RetAddress) =  serverSocket.recvfrom(2048)
    print(RetAddress)
    bytTostr = byteS.decode()

    upperCase = bytTostr.upper()

    strTobyte = upperCase.encode()

    serverSocket.sendto(strTobyte,RetAddress)
