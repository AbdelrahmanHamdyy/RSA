import math
import random

GROUP_SIZE = 5
PACKET_SIZE = 65535

def isPrime(num):
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generatePrimeNumber(numberOfBits):
    while True:
        num = random.randint(0, pow(2, numberOfBits // 2) - 1)
        if isPrime(num):
            return num
 
def generatePublicKey(numberOfBits):
    # Generate p & q
    p = generatePrimeNumber(numberOfBits)
    q = generatePrimeNumber(numberOfBits)
    print("p & q Generated")
    
    # Calculate n & phiN
    n = p * q
    phiN = (p - 1) * (q - 1)
    
    # Generate e
    e = random.randint(1, phiN - 1)
    while math.gcd(e, phiN) != 1:
        e = random.randint(1, phiN - 1)
    print("e Generated")
    
    # Set public key
    publicKey = (e, n)
    
    return publicKey, phiN

def generatePrivateKey(publicKey, phiN):
    e, n = publicKey
    
    # Compute d
    d = pow(e, -1, phiN)
    privateKey = (d, n)
    
    return privateKey
    
def generateKeys(numberOfBits):
    publicKey, phiN = generatePublicKey(numberOfBits)
    privateKey = generatePrivateKey(publicKey, phiN)
    return publicKey, privateKey

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

def processInput(msg):
    if (len(msg) % GROUP_SIZE != 0):
        msg += (" " * (((len(msg) // GROUP_SIZE + 1) * GROUP_SIZE) - len(msg)))
    return msg.lower()

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

def sendMsg(conn, publicKey):
    print("Start Chatting!")
    while True:
        msg = str(input())
        msg = processInput(msg)
        conn.send(str(len(msg) // GROUP_SIZE).encode())
        
        index = 0
        for i in range(len(msg) // GROUP_SIZE):
            C = encrypt(msg[index: index+GROUP_SIZE], publicKey)
            conn.send(str(C).encode())
            index += GROUP_SIZE
            
        if ("bye" in msg):
            break

def receiveMsg(conn, privateKey):
    while True:
        numberOfPackets = conn.recv(PACKET_SIZE).decode()
        
        result = ""
        for i in range(int(numberOfPackets)):
            C = conn.recv(PACKET_SIZE).decode()
            M = decrypt(int(C), privateKey)
            result += M
            
        print("-->", result, flush=True)
        if ("bye" in result):
            break