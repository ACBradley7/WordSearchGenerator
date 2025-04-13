# ENHANCEMENTS:
# - Add support to make grid a rectangle
# - Front end GUI: Input words, grid size, title, reciever email address
# - Errors/Exceptions

import smtplib
import random
import string
import fpdf
from termcolor import colored
from email.message import EmailMessage

class Letter:
    def __init__(self, letter: str, isPlaced: bool, color: str) -> None:
        self.letter = letter
        self.isPlaced = isPlaced
        self.color = color

def createGrid(gridLength) -> list:
    grid = [[Letter(random.choice(string.ascii_letters).upper(), False, "white") for x in range(gridLength)] for y in range(gridLength)]
    return grid
    
def dispGrid(grid: list) -> None:
    print()
    gridRow = ""
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            gridRow = gridRow + colored(grid[x][y].letter, grid[x][y].color) + " "
        print(gridRow)
        gridRow = ""

def wordCheckRecursion(grid: list, gridLength: int, word: str, skipDiagonals: bool, skipBackwards: bool) -> None:
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

def caseCheckInformation(grid: list, gridLength: int, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int) -> bool:
    if wordCheckInGrid(grid, gridLength, word, startRowIndex, startColIndex, rowFactor, colFactor):
        putWord(grid, word, startRowIndex, startColIndex, rowFactor, colFactor)
        return False
    else:
        return True

def wordCheckInGrid(grid: list, gridLength: int, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int) -> bool:
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

def putWord(grid: list, word: str, startRowIndex: int, startColIndex: int, rowFactor: int, colFactor: int) -> None:
        for index in range(len(word)):
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].letter = word[index]
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].isPlaced = True
            grid[startRowIndex + index * rowFactor][startColIndex + index * colFactor].color = "red"

def generateDirection(skipDiagonals: bool, skipBackwards: bool) -> int:
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

def createPDF() -> fpdf:
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    return pdf

def gridToPDF(pdf: fpdf, array: list, wordsArr: list) -> string:
    spacing = 6

    startPositionX = findGridPositionX(pdf, array, spacing)
    startPositionY = findGridPositionY(pdf)

    makeStudentVersion(pdf, array, startPositionX, startPositionY, spacing)
    displayWordList(pdf, wordsArr)
    pdf.add_page()
    makeTeacherVersion(pdf, array, startPositionX, startPositionY, spacing)

    filePath = "WordSearch.pdf"
    pdf.output(filePath)

    return filePath

def findGridPositionX(pdf: fpdf, array: list, spacing: int) -> float:
    outputLeftEdge = pdf.get_x()
    outputRightEdge = pdf.get_x() + len(array[0]) * spacing

    outputWidth = outputRightEdge - outputLeftEdge
    pageWidth = pdf.w
    
    startPositionX = (pageWidth - outputWidth) / 2.0
    return startPositionX

def findGridPositionY(pdf: fpdf) -> float:
    pageHeight = pdf.h
    startPositionY = pageHeight / 7.0

    return startPositionY

def makeStudentVersion(pdf: fpdf, array: list, startPositionX: float, startPositionY: float, spacing: int) -> None:
    makeGridBorder(pdf, array, startPositionX, startPositionY, spacing)
    pdf.set_y(startPositionY)
    for i in range(len(array)):
        pdf.set_x(startPositionX)
        for j in range(len(array[i])):
            pdf.cell(spacing, spacing, array[i][j].letter, 0, 0, "C", False)
        pdf.ln()

def displayWordList(pdf: fpdf, wordsArr: list) -> None:
    borderWidth = pdf.w * 3.0 / 4.0
    borderHeight = pdf.h / 4.0
    xSpacing = borderWidth / 5.0
    ySpacing = borderHeight / 6.0
    xOffset = xSpacing / 4.0
    counter = 1
    width = 15
    height = 8
    wordsPerLine = 5
    
    startPosX = (pdf.w - borderWidth) / 2.0
    posY = pdf.h - pdf.h * 2.0 / 5.0

    pdf.set_line_width(0.5)
    pdf.rect(startPosX, posY, borderWidth, borderHeight, "D")

    posY += ySpacing / 2.0
    startPosX = (pdf.w - borderWidth) / 2.0 + xOffset

    for i in range(len(wordsArr)):
        if i % wordsPerLine == 0:
            pdf.set_y(posY)
            posY += ySpacing
            pdf.set_x(startPosX)
            counter = 1
        pdf.cell(width, height, wordsArr[i], 0, 0, "C", False)
        newPosX = startPosX + xSpacing * counter
        counter += 1
        pdf.set_x(newPosX)

def makeTeacherVersion(pdf: fpdf, array: list, startPositionX: float, startPositionY, spacing: int) -> None:
    makeGridBorder(pdf, array, startPositionX, startPositionY, spacing)
    pdf.set_y(startPositionY)
    for i in range(len(array)):
        pdf.set_x(startPositionX)
        for j in range(len(array[i])):
            if array[i][j].color == "red":
                pdf.cell(spacing, spacing, array[i][j].letter, 0, 0, "C", False)
            else:
                pdf.cell(spacing, spacing, "-", 0, 0, "C", False)
        pdf.ln()

def makeGridBorder(pdf: fpdf, grid: list, startPositionX: float, startPositionY: float, spacing: int) -> None:
    makeEllipseHeader(pdf)
    pdf.set_line_width(0.5)
    startPosX = startPositionX - spacing
    startPosY = startPositionY - spacing
    width = (len(grid) + 2) * spacing
    height = (len(grid[0]) + 2) * spacing
    pdf.rect(startPosX, startPosY, width, height, "D")

def makeEllipseHeader(pdf: fpdf) -> None:
    pdf.set_line_width(0.5)
    
    horiRadius = 80
    vertRadius = 20
    centerX = (pdf.w / 2.0) - (horiRadius / 2.0)
    centerY = (pdf.h / 13.0) - (vertRadius / 2.0)

    #pdf.ellipse(centerX, centerY, horiRadius, vertRadius, "D")
    makeEllipseTitle(pdf, centerX, centerY, vertRadius, "Word Search")

def makeEllipseTitle(pdf: fpdf, startPositionX: float, startPositionY: float, vertRadius: float, title: string) -> None:
    pdf.set_font("Arial", size=20)
    cellHeight = 10

    strWidth = pdf.get_string_width(title)
    startPosX = startPositionX + (strWidth / 2.0)
    startPosY = startPositionY + (vertRadius / 2.0) - (cellHeight / 2.0)

    pdf.set_xy(startPosX, startPosY)
    pdf.cell(strWidth, 10, title, 0, 0, "C", False)
    titleUnderline(pdf, startPosX, startPosY, strWidth, 8)

    pdf.set_font("Arial", size=12)

def titleUnderline(pdf: fpdf, startPositionX: float, startPositionY: float, strWidth: float, offset: int) -> None:
    pdf.set_line_width(0.5)
    pdf.line(startPositionX, startPositionY + offset, startPositionX + strWidth, startPositionY + offset)

def sendEmail(pdf: fpdf, recieverEmail: string, path: string) -> None:
    sender_email = "dummywordsearch@gmail.com"
    receiver_email = recieverEmail
    subject = "Word Search PDF"
    body = "Please find the attached PDF file."
    password = "tyxx iubt sese wezl"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    pdf_path = path
    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(sender_email, password)
    smtp_server.send_message(msg)

def main() -> None:
    gridLength = 18
    wordsList = ["Angle", "Geometry", "Acute", "Obtuse", "Right", "Straight", "Congruent", "Vertex", "Vertical", "Adjacent", "Interior", "Exterior"]
    recieverEmail = "acbradley7@gmail.com"

    # Skip Dirs: 5, 6, 7, 8
    skipDiagonals = False
    # Skip Dirs: 4, 5, 8
    skipBackwards = False

    grid = createGrid(gridLength)
    
    for word in wordsList:
        wordCheckRecursion(grid, gridLength, word, skipDiagonals, skipBackwards)    

    dispGrid(grid)

    pdf = createPDF()
    filePath = gridToPDF(pdf, grid, wordsList)
    sendEmail(pdf, recieverEmail, filePath)

main()