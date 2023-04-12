import RSA
import socket
import threading

HOST = socket.gethostname()
PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runClient():
    clientSocket.connect((HOST, PORT))
    print("Client connected..", flush=True)
    numberOfBits = clientSocket.recv(RSA.PACKET_SIZE).decode()
    print("Client: Number of bits received", flush=True)
    
    publicKey, privateKey = RSA.generateKeys(int(numberOfBits))
    print("Client: Keys generated", flush=True)

    PU = clientSocket.recv(RSA.PACKET_SIZE).decode()
    PU = PU.split()
    e = int(PU[0])
    n = int(PU[1])
    print("Client: PU received", flush=True)
    
    clientSocket.send(' '.join(str(x) for x in publicKey).encode())
    print("Client: PU sent", flush=True)
    
    T1 = threading.Thread(target=RSA.sendMsg, args=(clientSocket, (e, n)))
    T2 = threading.Thread(target=RSA.receiveMsg, args=(clientSocket, privateKey))
    T1.start()
    T2.start()

    T1.join()
    T2.join()
    
    clientSocket.close()
    print("Client Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runClient()
    