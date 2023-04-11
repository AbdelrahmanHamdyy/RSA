import RSA
import socket

HOST = socket.gethostname()
PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runClient():
    publicKey, privateKey = RSA.generateKeys()
    turn = 1
    
    clientSocket.connect((HOST, PORT))
    print("Client connected.. Start Chatting!")
    
    PU = RSA.receivePublicKey(clientSocket)
    RSA.sendPublicKey(clientSocket, publicKey)
    
    while True:
        result = RSA.send(clientSocket, PU) if turn else RSA.receive(clientSocket, privateKey)
        if (not result):
            break
        
        turn ^= 1
        
    clientSocket.close()
    print("Client Side: Connection Closed!")

if __name__ == '__main__':
    runClient()
    