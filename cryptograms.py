"""
    cryptograms
    ~~~~~~~~
    a console application that entertains user with cryptogram games

    :copyright: (c) 2017 Shanshan Wang
    :license: MIT
"""

import csv
import random
import os

difficulty = 3 # control the number of letters being replaced in the cryptogram.
datafilePath = 'data/quotes.csv'

def loadData(idx, datafilePath = datafilePath):
    # load a quote from \data\quotes.csv
    with open(datafilePath, newline='',encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if reader.line_num==idx:
                quote = row[1]
                author = row[2]
                return [quote, author]
            else:
                continue

def genKeys(original, difficulty):
    # generate character mapping for encryption
    characterSet = [x for x in set(original.lower()) if x.isalpha()]
    nKeys = min(difficulty, len(characterSet))

    #generate characters to be replaced
    keys = random.sample(characterSet, nKeys)

    # generate replacing characters
    # note that all values are lowercases
    keyMap={}
    forbiddenVal = [ord(x) for x in characterSet]
    for key in keys:
        keyMap[key] = chr(random.sample([i for i in range(ord('a'), ord('z')) if i not in forbiddenVal],1)[0])
        forbiddenVal.remove(ord(key))
        forbiddenVal.append(ord(keyMap[key]))

    return keyMap

def getUserKeys(keyMap):
    # reverse key and value pairs in keyMap to generate the game answer
    userKeys= {}
    for key in keyMap:
        userKeys[keyMap[key]]= key
    return userKeys

def encrypt(original, keyMap):
    encryptedList = list(original)

    for i in range(0,len(original)):
        if (original[i].lower() in keyMap):
            key = original[i].lower()
            value = keyMap[key].lower()
            if (original[i].islower()):
                encryptedList[i] = value
            else:
                encryptedList[i] = value.upper()
    encrypted = ''.join(encryptedList)
    return encrypted

def score(userInputs,userKeys):
    total = len(userInputs)
    correctCnt =0
    wrongCnt = 0

    for key in userKeys:
        if key in userInputs and userKeys[key].lower()==userInputs[key].lower():
            correctCnt +=1
        else:
            wrongCnt +=1

    if wrongCnt == 0:
        return "You got it!"
    elif wrongCnt == 1:
        return "So close!"
    else:
        return "Try again!"

if __name__ == "__main__":

    # Uncomment the next line to use a fixed random seed
    # random.seed(a=0)

    while True:

        idx =random.randint(0, 1000)    #1000 is the number of quotes in the datafile
        print('game id = ' + str(idx))
        [original, author] = loadData(idx)

        print(author)
        keyMap = genKeys(original, difficulty)

        encrypted = encrypt(original,keyMap)
        print(encrypted)

        userKeys = getUserKeys(keyMap)

        print()
        input("Press enter when you are ready to crack the encrytogram...")
        userInputs={}

        for key in userKeys:
            ans = input(key + "=")
            userInputs[key]=str(ans)

        print()
        print("your answer=")
        print(encrypt(encrypted,userInputs))

        print()
        print('correct answer=')
        print(original)
        print(userKeys)

        print("****************" + score(userInputs,userKeys) + "****************")

        print()
        yorn =input("Play another one(y/n)?")
        if yorn.lower()=='y':
            os.system('cls' if os.name == 'nt' else 'clear') # clear the window
            continue
        else:
            break
