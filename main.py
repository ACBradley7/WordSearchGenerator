import random
import os
import math
import string
import json
import numpy as np
from PIL import Image as im
from termcolor import colored

class Letter:
    def __init__(self, letter: str, isPlaced: bool, color: str):
        self.letter = letter
        self.isPlaced = isPlaced
        self.color = color

def createGrid(gridLength):
    grid = [[Letter(random.choice(string.ascii_letters).upper(), False, "white") for x in range(gridLength)] for y in range(gridLength)]
    return grid
    
def dispGrid(grid: list):
    print()
    gridRow = ""
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            gridRow = gridRow + colored(grid[x][y].letter, grid[x][y].color) + " "
        print(gridRow)
        gridRow = ""

def wordCheckRecursion(grid: list, gridLength: int, word: str, skipDiagonals: bool, skipBackwards: bool):
    word = word.upper()
    wordLegnth = len(word)
    needsRecursion = True
    
    startRowIndex = random.randint(0, gridLength - 1)
    startColIndex = random.randint(0, gridLength - 1)
    
    direction = generateDirection(skipDiagonals, skipBackwards)
    
    match direction:
        # Up
        case 1:
            if startRowIndex + 1 - (len(word)) >= 0:
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, -1, 0)
        # Right
        case 2:
            if startColIndex + (len(word)) <= len(grid):
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, 0, 1)
        # Down
        case 3:
            if startRowIndex + (len(word)) <= len(grid[0]):
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, 1, 0)
        # Left
        case 4:
            if startColIndex + 1 - (len(word)) >= 0:
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, 0, -1)
        # Up / Left
        case 5:
            if startRowIndex + 1 - (len(word)) >= 0 and startColIndex + 1 - (len(word)) >= 0:
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, -1, -1)
        # Up / Right
        case 6:
            if startRowIndex + 1 - (len(word)) >= 0 and startColIndex + (len(word)) <= len(grid):
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, -1, 1)
        # Down / Right
        case 7:
            if startRowIndex + (len(word)) <= len(grid[0]) and startColIndex + (len(word)) <= len(grid):
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, 1, 1)
        # Down / Left
        case 8:
            if startRowIndex + (len(word)) <= len(grid[0]) and startColIndex + 1 - (len(word)) >= 0:
                needsRecursion = caseCheckInformation(grid, gridLength, word, startRowIndex, startColIndex, 1, -1)

    if needsRecursion:
        return wordCheckRecursion(grid, gridLength, word, skipDiagonals, skipBackwards)

def caseCheckInformation(grid: list, gridLength: int, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int):
    if wordCheckInGrid(grid, gridLength, word, startRowIndex, startColIndex, rowFactor, colFactor):
        putWord(grid, word, startRowIndex, startColIndex, rowFactor, colFactor)
        return False
    else:
        return True

def wordCheckInGrid(grid: list, gridLength: int, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int):
    valid = False
    for index in range(len(word)):
        if grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].letter == word[index]:
            # Hit a previously placed word but the letters match. Can put this word here.
            valid = True
        elif grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].isPlaced == True:
            # Hit a previously placed word. Cannot put this word here.
            valid = False
            break
        else:
            # Did not hit a placed word. Can put this word here.
            valid = True
    return valid

def putWord(grid: list, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int):
        for index in range(len(word)):
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].letter = word[index]
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].isPlaced = True
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].color = "red"

def generateDirection(skipDiagonals: bool, skipBackwards: bool):
    if skipDiagonals and skipBackwards:
        direction = random.randint(1, 3)
    elif skipDiagonals:
        direction = random.randint(1, 4)
    elif skipBackwards:
        dirs = [1, 2, 3, 6, 7]
        direction = random.choice(dirs)
    else:
        direction = random.randint(1,8)
    return direction

def getCounter():
    with open("newFileCounter.json", "r") as file:
        data = json.load(file)
        counter = data["counter"]
    return counter
    
def storeCounter(counter: int):
    with open("newFileCounter.json", "w") as file:
        data = {
            "counter": counter
        }
        json.dump(data, file)
        
def textToImage(fileCounter: int):
    None

def main():
    gridLength = 12
    wordsList = ["Dragon", "Gold", "Fire", "Hero"]
    
    # Skip Dirs: 5, 6, 7, 8
    skipDiagonals = False
    # Skip Dirs: 4, 5, 8
    skipBackwards = False

    grid = createGrid(gridLength)
    
    for word in wordsList:
        wordCheckRecursion(grid, gridLength, word, skipDiagonals, skipBackwards)    

    dispGrid(grid)
    
    #grid = np.arange(0, 737280, 1, np.uint8)
    #grid = np.reshape(grid, (1024, 720))
    #data = im.fromarray(grid)
    #data.save('gfg_dummy_pic.png')
    
    counter = getCounter()
    
    print()
    print(counter)
    
    counter += 1
    storeCounter(counter)

main()