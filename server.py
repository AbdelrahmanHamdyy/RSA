import RSA
import socket
import threading

HOST = socket.gethostname()
PORT = 5000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runServer():
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    print(f"Server is listening on {HOST}:{PORT}", flush=True)
    conn, address = serverSocket.accept()
    print("Connection from: " + str(address), flush=True)
    
    numberOfBits = input("Key size (Number of bits): ")
    conn.send(numberOfBits.encode())
    print("Server: Number of bits sent", flush=True)
    
    publicKey, privateKey = RSA.generateKeys(int(numberOfBits))
    print("Server: Keys generated", flush=True)
    
    conn.send(' '.join(str(x) for x in publicKey).encode())
    print("Server: PU sent", flush=True)
    
    PU = conn.recv(RSA.PACKET_SIZE).decode()
    PU = PU.split()
    e = int(PU[0])
    n = int(PU[1])
    print("Server: PU received", flush=True)

    T1 = threading.Thread(target=RSA.sendMsg, args=(conn, (e, n)))
    T2 = threading.Thread(target=RSA.receiveMsg, args=(conn, privateKey))
    T1.start()
    T2.start()
        
    T1.join() 
    T2.join()
    
    conn.close()
    print("Server Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runServer()
    