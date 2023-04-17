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
    
    name = input("Name: ")
    conn.send(name.encode()) # Send name
    
    userName = conn.recv(RSA.PACKET_SIZE).decode() # Receive client's name
    
    publicKey, privateKey = RSA.generateKeys(int(RSA.KEY_SIZE)) # Generate Private and Public Keys

    conn.send(' '.join(str(x) for x in publicKey).encode()) # Send Public Key

    PU = conn.recv(RSA.PACKET_SIZE).decode() # Receive Public Key from the Client
    PU = PU.split()
    e, n = int(PU[0]), int(PU[1]) # Extract e & n

    T1 = threading.Thread(target=RSA.sendMsg, args=(conn, (e, n)))
    T2 = threading.Thread(target=RSA.receiveMsg, args=(conn, userName, privateKey))
    T1.start()
    T2.start()
        
    T1.join() 
    T2.join()
    
    conn.close()
    print("Server Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runServer()
    