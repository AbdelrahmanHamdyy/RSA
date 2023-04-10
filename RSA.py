import math
import random
import sys
import socket

HOST = socket.gethostname()
PORT = 5000
PACKET_SIZE = 1024

GROUP_SIZE = 5

def isPrime(num):
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generatePrimeNumber():
    while True:
        num = random.randint(0, pow(2, 32) - 1)
        if isPrime(num):
            return num
 
def generatePublicKey():
    # Generate p & q
    p = generatePrimeNumber()
    q = generatePrimeNumber()
    
    # Calculate n & phiN
    n = p * q
    phiN = (p - 1) * (q - 1)
    
    # Generate e
    e = random.randint(0, phiN - 1)
    while math.gcd(e, phiN) != 1:
        e = random.randint(0, phiN - 1)
    
    # Set public key
    publicKey = (e, n)
    
    return publicKey, phiN

def generatePrivateKey(publicKey, phiN):
    e, n = publicKey
    
    # Compute d
    d = pow(e, -1, phiN)
    privateKey = (d, n)
    
    return privateKey
    

def encode(plainText):
    numbers = []
    for char in plainText:
        asciiVal = ord(char)
        if (asciiVal >= 48 and asciiVal <= 57):
            numbers.append(asciiVal - 48)
        elif (asciiVal >= 97 and asciiVal <= 122):
            numbers.append(asciiVal - 87)
        else:
            numbers.append(36)
            
    result = 0
    for i in range(GROUP_SIZE):
        result += (numbers[i] * pow(37, GROUP_SIZE - 1 - i))
    
    return result
    
    
def decode(decryptedText):
    result = ""
    N = decryptedText
    for i in range(GROUP_SIZE):
        div = N // pow(37, GROUP_SIZE - 1 - i)
        mod = N % pow(37, GROUP_SIZE - 1 - i)
        if (div <= 9):
            result += str(div)
        elif (div >= 10 and div <= 35):
            result += chr(div + 87)
        else:
            result += " "
        N = mod
        
    return result

def encrypt(plainText, publicKey):
    encodedText = encode(plainText)
    e, n = publicKey
    cipherText = pow(encodedText, e, n)
    return cipherText

def decrypt(cipherText, privateKey):
    d, n = privateKey
    decryptedText = pow(cipherText, d, n)
    plainText = decode(decryptedText)
    return plainText

def RSA(plainText):
    publicKey, privateKey = generateKeys()
    
    if (len(plainText) % 5 != 0):
        plainText += (" " * (((len(plainText) // 5 + 1) * 5) - len(plainText)))
        
    result = ""
    index = 0
    for i in range(len(plainText) // 5):
        C = encrypt(plainText[index: index+5], publicKey)
        M = decrypt(C, privateKey)
        result += M
        index += 5
        
    return result

def run():
    send = 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        publicKey, phiN = generatePublicKey()
        privateKey = generatePrivateKey(publicKey, phiN)
        Type = sys.argv[1]
        PU = "PublicKey"
        conn = "Connection"
        if (Type == "1"): # Server
            send = 0
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"Server is listening on {HOST}:{PORT}")
            conn, address = s.accept()
            print("Connection from: " + str(address))
            conn.send(str(publicKey[0]).encode())
            conn.send(str(publicKey[1]).encode())
            e = int(conn.recv(PACKET_SIZE).decode())
            n = int(conn.recv(PACKET_SIZE).decode())
            PU = (e, n)
        else:
            s.connect((HOST, PORT))
            e = int(s.recv(PACKET_SIZE).decode())
            n = int(s.recv(PACKET_SIZE).decode())
            PU = (e, n)
            s.send(str(publicKey[0]).encode())
            s.send(str(publicKey[1]).encode())
            
        while True:
            if (send):
                msg = str(input("You: "))
                if (len(msg) % 5 != 0):
                    msg += (" " * (((len(msg) // 5 + 1) * 5) - len(msg)))
                index = 0
                N = str(len(msg) // 5).encode()
                conn.send(N) if Type == "1" else s.send(N)
                for i in range(len(msg) // 5):
                    C = encrypt(msg[index: index+5].lower(), PU)
                    conn.send(str(C).encode()) if Type == "1" else s.send(str(C).encode())
                    index += 5
                send ^= 1
                if (msg == "bye  "):
                    break
            else:
                numberOfPackets = conn.recv(PACKET_SIZE).decode() if Type == "1" else s.recv(PACKET_SIZE).decode()
                result = ""
                for i in range(int(numberOfPackets)):
                    C = conn.recv(PACKET_SIZE).decode() if Type == "1" else s.recv(PACKET_SIZE).decode()
                    M = decrypt(int(C), privateKey)
                    result += M
                print("User: ", result)
                if (result == "bye  "):
                    break
                send ^= 1
        
        print("Connection Closed!")
        conn.close() if Type == "1" else s.close()

if __name__ == '__main__':
    run()