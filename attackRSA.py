import math
import RSA

GROUP_SIZE = RSA.GROUP_SIZE

def factorizeN(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if RSA.isPrime(i) and n % i == 0:
            return i, n // i
        
def getPrivateKey(publicKey):
    e, n = publicKey
    p, q = factorizeN(n)
    phiN = (p - 1) * (q - 1)
    d = pow(e, -1, phiN)
    return d, n

def attack(cipherText, publicKey):
    privateKey = getPrivateKey(publicKey)
    plainText = RSA.decrypt(cipherText, privateKey)
    return plainText

if __name__ == '__main__':
    numberOfBits = int(input("Key size (Number of bits): "))
    plainText = input("Plain Text: ");
    plainText = RSA.processInput(plainText)
    publicKey, phiN = RSA.generatePublicKey(numberOfBits)
    index = 0
    result = ""
    for i in range(len(plainText) // GROUP_SIZE):
        cipherText = RSA.encrypt(plainText[index: index+GROUP_SIZE], publicKey)
        result += attack(cipherText, publicKey)
        index += GROUP_SIZE 
    print("Result: ", result)