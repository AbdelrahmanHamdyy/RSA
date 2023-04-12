import RSA
import socket

HOST = socket.gethostname()
PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runClient():
    clientSocket.connect((HOST, PORT))
    print("Client connected.. Start Chatting!", flush=True)
    numberOfBits = clientSocket.recv(RSA.PACKET_SIZE).decode()
    print("Client: Number of bits received", flush=True)
    
    publicKey, privateKey = RSA.generateKeys(int(numberOfBits))
    print("Client: Keys generated")
    turn = 0
    
    print("Client: Receiving PU..", flush=True)
    e = int(clientSocket.recv(RSA.PACKET_SIZE).decode())
    n = int(clientSocket.recv(RSA.PACKET_SIZE).decode())
    PU = (e, n)
    print("Client: PU received", flush=True)
    print("Client: Sending PU..", flush=True)
    clientSocket.send(str(publicKey[0]).encode()) # Send e
    clientSocket.send(str(publicKey[1]).encode()) # Send n
    print("Client: PU sent", flush=True)
    
    while True:
        result = RSA.sendMsg(clientSocket, PU) if turn else RSA.receiveMsg(clientSocket, privateKey)
        if (not result):
            break
        
        turn ^= 1
        
    clientSocket.close()
    print("Client Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runClient()
    