import RSA
import socket

HOST = socket.gethostname()
PORT = 5000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def runServer():
    publicKey, privateKey = RSA.generateKeys()
    turn = 0
    
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    conn, address = serverSocket.accept()
    print("Connection from: " + str(address))
    
    RSA.sendPublicKey(conn, publicKey)
    PU = RSA.receivePublicKey(conn)
    
    while True:
        result = RSA.send(conn, PU) if turn else RSA.receive(conn, privateKey)
        if (not result):
            break
        
        turn ^= 1
        
    conn.close()
    print("Server Side: Connection Closed!")

if __name__ == '__main__':
    runServer()
    