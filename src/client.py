import RSA
import socket
import threading

HOST = socket.gethostname()
PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runClient():
    clientSocket.connect((HOST, PORT))
    print("Client connected..", flush=True)
    userName = clientSocket.recv(RSA.PACKET_SIZE).decode() # Receive server's name
    
    name = input("Name: ")
    clientSocket.send(name.encode()) # Send name
    
    publicKey, privateKey = RSA.generateKeys(int(RSA.KEY_SIZE)) # Generate Private and Public Key

    PU = clientSocket.recv(RSA.PACKET_SIZE).decode() # Receive Public Key from the Server
    PU = PU.split()
    e, n = int(PU[0]), int(PU[1]) # Extract e & n

    clientSocket.send(' '.join(str(x) for x in publicKey).encode()) # Send Public Key
    
    T1 = threading.Thread(target=RSA.sendMsg, args=(clientSocket, (e, n)))
    T2 = threading.Thread(target=RSA.receiveMsg, args=(clientSocket, userName, privateKey))
    T1.start()
    T2.start()

    T1.join()
    T2.join()
    
    clientSocket.close()
    print("Client Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runClient()
    