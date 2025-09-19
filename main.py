from tkinter import *
import tkinter.messagebox

# GUI settings ----------------------------------------------------------

margin = 4              # define margin of main grid
gridSize = 9            # define the number of squares in the grid
squareSize = 40         # define the size of individual squares
borderSize = 30         # define the border size between canvas and main window
gridLength = (gridSize * squareSize) + margin
windowSize = gridLength + (2 * borderSize)
winSizeString = str(windowSize) + "x" + str(windowSize+100)
highlightWidth = 4

buttonGridHeight = 80
buttonMargin = 10
buttonWidth = 70
buttonHeight = 40
buttonColor = "#dddddd"
buttonColorPressed = "#555555"
buttonPressTime = 10

# Algorithm initial settings ----------------------------------------------------------

inputArray = [0] * (gridSize * gridSize)
inputIndex = 0
inputIndexLast = inputIndex
outputArray = inputArray.copy()
outputArrayLast = outputArray.copy()
running = True

solving = False
instaSolving = False
solved = False
pointer = 0
direction = 1
firstIndex = 0
lastIndex = 0

# Functions ----------------------------------------------------------

def checkRowColBox(number, index, grid):
    notInRow, notInCol, notInCell = True, True, True
    # Check row
    rowStart = int(index / 9) * 9
    for i in range(rowStart, rowStart + 9):
        if grid[i] == number: notInRow = False
    # Check column
    colStart = index % 9
    for i in range(colStart, (colStart + 72) + 1, 9):
        if grid[i] == number: notInCol = False
    # Check cell
    cellRow = int(index / 27)
    cellCol = int((index % 9) / 3)
    cellStart = (cellRow * 27) + (cellCol * 3)
    for i in range(cellStart, cellStart + 3):
        if grid[i] == number or grid[i + 9] == number or grid[i + 18] == number: notInCell = False
    return notInRow and notInCol and notInCell

def solve():                # Trigger the solving algorithm and initialise all relevant variables
    global solving, solved, firstIndex, lastIndex, pointer, direction, outputArray, inputArray, inputSquare
    if not solving and not solved:
        inputArray = outputArray.copy()
        solving, solved, pointer, direction = True, False, 0, 1
        firstIndex = outputArray.index(0)
        lastIndex = 80 - outputArray[::-1].index(0)
        mainGrid.delete(inputSquare)

def instaSolve():
    global solving, solved, instaSolving, firstIndex, lastIndex, pointer, direction, outputArray, inputArray, inputSquare
    if not solving and not solved:
        inputArray = outputArray.copy()
        solving, instaSolving, solved, pointer, direction = True, True, False, 0, 1
        firstIndex = outputArray.index(0)
        lastIndex = 80 - outputArray[::-1].index(0)
        mainGrid.delete(inputSquare)

def reset():
    global solving, instaSolving, solved, outputArray, inputArray, resultText, inputIndexLast
    solving, instaSolving, solved = False, False, False
    outputArray = inputArray.copy()
    resultText.set("")
    inputIndexLast = -1                 # since this no longer matches inputIndex, the input square is redrawn

def clear():
    global solving, instaSolving, solved, outputArray, inputArray, inputIndexLast
    answer = tkinter.messagebox.askquestion("Clear", "Are you sure you want to clear the grid?")
    if answer == "yes":
        inputArray = [0] * 81
        outputArray = inputArray.copy()
        inputIndexLast = -1  # since this no longer matches inputIndex, the input square is redrawn
        solving, instaSolving, solved = False, False, False
        resultText.set("")
    elif answer == "no":
        pass

def leftClick(event):                   # selects a box for editing
    global inputIndex, solving
    x, y = event.x, event.y
    if not solving:
        xCo = int(x / squareSize)
        yCo = int(y / squareSize)
        if yCo < 9:
            inputIndex = (yCo * 9) + xCo
    if y > y0 and y < y1:               # detects GUI button clicks
        if x > x0 and x < x1:
            buttonCounters[0] = buttonPressTime
            solve()
        elif x > x2 and x < x3:
            buttonCounters[1] = buttonPressTime
            instaSolve()
        elif x > x4 and x < x5:
            buttonCounters[1] = buttonPressTime
            reset()
        elif x > x6 and x < x7:
            buttonCounters[2] = buttonPressTime
            clear()

def keyInput(event):
    global inputIndex, outputArray, solving
    if not solving:
        num = event.keysym
        if num == "BackSpace":
            outputArray[inputIndex] = 0
        elif num == "Left":
            if inputIndex % 9 > 0:
                inputIndex -= 1
        elif num == "Right":
            if inputIndex % 9 < 8:
                inputIndex += 1
        elif num == "Up":
            if int(inputIndex / 9) > 0:
                inputIndex -= 9
        elif num == "Down":
            if int(inputIndex / 9) < 8:
                inputIndex += 9
        else:
            try:
                num = int(num)
                outputArray[inputIndex] = num
            except:
                print("Please enter a number. No other characters allowed.")
        #print(num)

# Create interface ----------------------------------------------------------------

window = Tk()
window.title("Sudoku")
window.geometry(winSizeString)

# Create main grid
mainGrid = Canvas(window, width=gridLength-1, height=gridLength-1+buttonGridHeight, bg="white")
mainGrid.pack(pady=10)

# Create key and mouse-button bindings
mainGrid.bind("<Button-1>", leftClick)      # left mouse click
window.bind("<Key>", keyInput)              # key input

# Draw grid
for i in range(gridSize+1):
    lineCo = (i * squareSize) + margin
    if i % 3 == 0:
        thickness = 3
        colour = "black"
    else:
        thickness = 1
        colour = "grey"
    mainGrid.create_line(lineCo, 0, lineCo, gridLength+1, fill=colour, width=thickness)
    mainGrid.create_line(0, lineCo, gridLength+1, lineCo, fill=colour, width=thickness)

# Create initial input box lines
inputSquare = mainGrid.create_rectangle(margin, margin, squareSize+margin, squareSize+margin, width=4, outline="green")

# Create solve, instaSolve, reset and clear buttons
buttonGrid = mainGrid.create_rectangle(margin-1,gridLength+1,gridLength+1,gridLength+buttonGridHeight+1, fill="grey")
x0 = buttonMargin
y0 = 2*buttonMargin + gridLength
x1 = x0 + buttonWidth
x2 = x1 + buttonMargin
x3 = x2 + buttonWidth
x4 = x3 + buttonMargin
x5 = x4 + buttonWidth
x7 = gridLength - buttonMargin
x6 = x7 - buttonWidth
y1 = y0 + buttonHeight
buttons = [0] * 4
buttonCounters = [0] * 4
textX0 = (x0+x1) / 2
textX1 = (x2+x3) / 2
textX2 = (x4+x5) / 2
textX3 = (x6+x7) / 2
textY = (y0+y1) / 2
buttonFont = ("Arial", "14", "bold")
buttons[0] = mainGrid.create_rectangle(x0,y0,x1,y1, fill=buttonColor)
buttons[1] = mainGrid.create_rectangle(x2,y0,x3,y1, fill=buttonColor)
buttons[2] = mainGrid.create_rectangle(x4,y0,x5,y1, fill=buttonColor)
buttons[3] = mainGrid.create_rectangle(x6,y0,x7,y1, fill=buttonColor)
solveText = mainGrid.create_text(textX0, textY, text="SOLVE", fill="black", font=buttonFont)
instaSolveText = mainGrid.create_text(textX1, textY, text = "QUICK\nSOLVE", fill="black", font=buttonFont)
resetText = mainGrid.create_text(textX2, textY, text="RESET", fill="black", font=buttonFont)
clearText = mainGrid.create_text(textX3, textY, text="CLEAR", fill="black", font=buttonFont)

# Create text output for when puzzle is solved
resultText = StringVar()
resultLabel = Label(window, height=10, width=100, padx=2, pady=2, textvariable=resultText)
resultLabel.pack()

# Create text array for numbers on screen
textArray = [mainGrid.create_text(0, 0, text="")] * 81

# Main program loop ---------------------------------------------------------------------------

while running:
    # Update pressed buttons
    for i in range(0,3):
        if buttonCounters[i] > 0:
            buttonCounters[i] -= 1
            mainGrid.itemconfig(buttons[i], fill=buttonColorPressed)
        else:
            mainGrid.itemconfig(buttons[i], fill=buttonColor)
    # Update highlighted input square
    if inputIndex != inputIndexLast:
        mainGrid.delete(inputSquare)
        squareX = inputIndex % 9
        squareY = int(inputIndex / 9)
        left = (squareX * squareSize) + margin
        top = (squareY * squareSize) + margin
        right = left + squareSize
        bottom = top + squareSize
        inputSquare = mainGrid.create_rectangle(left, top, right, bottom, width=4, outline="green")
    inputIndexLast = inputIndex
    # Update numbers on screen
    if outputArray != outputArrayLast:
        for i in range(len(outputArray)):
            if outputArray[i] != outputArrayLast[i]:
                mainGrid.delete(textArray[i])
                xCo = ((i % 9) * squareSize) + (squareSize / 2) + margin
                yCo = (int(i / 9) * squareSize) + (squareSize / 2) + margin
                if solving:
                    colour = "grey"
                    numFont = ("Helvetica", "20")
                else:
                    colour = "black"
                    numFont = ("Helvetica", "24", "bold")
                if outputArray[i] != 0:
                    textArray[i] = mainGrid.create_text(xCo, yCo, text=str(outputArray[i]), fill=colour, font=numFont)
        outputArrayLast = outputArray.copy()
    # Solving algorithm
    if solving and not solved:
        number = outputArray[pointer]
        if inputArray[pointer] > 0:               # skip over any initialised squares
            print("Initialized cell")
            pass
        elif number >= 9:                   # if square has been previously maxed out, reset it and move pointer back
            outputArray[pointer] = 0
            direction = -1
            print("Moving back")
            if pointer == firstIndex:       # if you find yourself back at the beginning, the puzzle can't be solved
                resultText.set("This Sudoku cannot be solved.")
                solving = False
        elif number >= 0:
            print("Incrementing box")
            number += 1
            if checkRowColBox(number, pointer, outputArray):
                outputArray[pointer] = number
                direction = 1
                print("Moving forward")
                if pointer == lastIndex:    # if this is the last square to complete, then the puzzle is solved
                    solved = True
                    instaSolving = False
                    resultText.set("This Sudoku has been solved.")
            else:
                outputArray[pointer] = number
                direction = 0
                print("Staying in place")
        pointer += direction

    if not instaSolving:
        window.update()



window.mainloop()
