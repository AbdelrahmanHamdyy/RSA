import math
import random

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
 
def generateKeys():
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
    
    # Compute d
    d = pow(e, -1, phiN)
    
    # Set public & private keys
    publicKey = (e, n)
    privateKey = (d, n)
    
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
    plainText = str(input("Enter Plain Text: "))
    result = RSA(plainText.lower())
    print("Decrypted Text: ", result)

if __name__ == '__main__':
    run()