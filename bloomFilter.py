# Bloom Filter

import hashlib
import random
from pylab import plot, show, xlabel, ylabel, legend

class bloomFilter:
    def __init__(self, vectorSize, *args):
        self.vectorSize = vectorSize
        self.vector = [0] * vectorSize
        self.hashFunctions = args

    def insert(self, value):
        for hashFunction in self.hashFunctions:
            self.vector[hashFunction(value) % self.vectorSize] = 1

    def contains(self, value):
        for hashFunction in self.hashFunctions:
            if self.vector[hashFunction(value) % self.vectorSize] == 0:
                return False
            else:
                return True

# Testing
def hashOne(value):
    hash = hashlib.sha256(value.encode())
    return int(hash.hexdigest(),base=16)

def hashTwo(value):
    hash = hashlib.sha384(value.encode())
    return int(hash.hexdigest(),base=16)

def hashThree(value):
    hash = hashlib.sha512(value.encode())
    return int(hash.hexdigest(),base=16)

def randomString(stringSize, alphabet):
    return ''.join(random.choice(alphabet) for i in range(stringSize))

def bloomTest(count, vectorSize):
    errors = 0
    bloom = bloomFilter(vectorSize, hashOne, hashTwo, hashThree)
    testCases = [randomString(10,"qwertyuiop") for i in range(count)]
    for word in testCases:
        bloom.insert(word)
    trueCases = testCases.copy()
    testCases += [randomString(10,"asdfghjklz") for i in range(count)]
    for word in testCases:
        if bloom.contains(word) and word not in trueCases:
            errors += 1
    return int(errors/(count)*100)

# Plot
vectorSizes = range(1,10000,100)
colors = ['green','brown','red']
pl,lg = [],[]
for count in range(100,301,100):
    errors = [bloomTest(count, vectorSize) for vectorSize in vectorSizes]
    pl += plot(vectorSizes,errors,color=colors[int(count / 100) - 1])
    lg += [str(count) + " elements | 3 hash"]
ylabel("percentage of errors %")
xlabel("size of bitarray")
legend(pl, lg, loc=1)
show()