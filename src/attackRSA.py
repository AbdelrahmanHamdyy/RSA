import math
import RSA

GROUP_SIZE = RSA.GROUP_SIZE

def factorizeN(n):
    if (n % 2 == 0):
        return 2, n // 2
    else:
        rootN = int(math.sqrt(n))
        if (rootN % 2 == 0):
            rootN -= 1
        for i in range(rootN, 2, -2):
            if RSA.isPrime(i) and n % i == 0:
                return i, n // i
        
def getPrivateKey(publicKey):
    e, n = publicKey
    p, q = factorizeN(n)
    phiN = (p - 1) * (q - 1)
    d = pow(e, -1, phiN)
    return d, n

def attack(plainText, publicKey, privateKey):
    index = 0
    result = ""
    for i in range(len(plainText) // GROUP_SIZE):
        cipherText = RSA.encrypt(plainText[index: index+GROUP_SIZE], publicKey)
        result += RSA.decrypt(cipherText, privateKey)
        index += GROUP_SIZE
    return result

if __name__ == '__main__':
    numberOfBits = int(input("Key size (Number of bits): "))
    plainText = input("Plain Text: ");
    plainText = RSA.processInput(plainText)
    
    publicKey, phiN = RSA.generatePublicKey(numberOfBits)
    actualPR = RSA.generatePrivateKey(publicKey, phiN);
    privateKey = getPrivateKey(publicKey)
    
    result = attack(plainText, publicKey, privateKey)
    
    print("Result: ", result)
    print("Success!") if (plainText == result and actualPR == privateKey) else print("Failed!")