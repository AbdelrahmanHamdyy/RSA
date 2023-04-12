import RSA
import socket

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
    print("Server: Keys generated")
    turn = 1
    
    print("Server: Sending PU..", flush=True)
    conn.send(str(publicKey[0]).encode()) # Send e
    conn.send(str(publicKey[1]).encode()) # Send n
    print("Server: PU sent", flush=True)
    print("Server: Receiving PU..", flush=True)
    e = int(conn.recv(RSA.PACKET_SIZE).decode())
    n = int(conn.recv(RSA.PACKET_SIZE).decode())
    PU = (e, n)
    print("Server: PU received", flush=True)
    
    while True:
        result = RSA.sendMsg(conn, PU) if turn else RSA.receiveMsg(conn, privateKey)
        if (not result):
            break
        
        turn ^= 1
        
    conn.close()
    print("Server Side: Connection Closed!", flush=True)

if __name__ == '__main__':
    runServer()
    