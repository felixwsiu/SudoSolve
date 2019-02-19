

# import the library
from appJar import gui
import copy
import stack
import time
import sudoparser


#fields/variables
progress = 0
count = 0
empties = 0
runtime = 0
limit = 1000
oldboards = stack.myStack() #a list of board that will be used to save board states if brute forcing is necessary


# handle button events
def clear(button):
    app.disableButton("Clear")
    clearboard()
    app.enableButton("Clear")
            
def clearboard():
    global runtime
    app.setMeter("Status",99.0,"Clearing")
    app.clearAllEntries(callFunction=False)
    for row in range(0,9):
        for col in range (0,9):
            app.setEntryFg(str(row)+str(col),"Black")
    app.setMeter("Status",0.0,"Idle")
    runtime = 0
            

def solve(button):
    app.disableButton("Solve")
    board = createboard()     #creates a list with all 9 rows based off input
    '''
    board = [
[0, 0, 6, 0, 5, 4, 9, 0, 0],
[1, 0, 0, 0, 6, 0, 0, 4, 2],
[7, 0, 0, 0, 8, 9, 0, 0, 0],
[0, 7, 0, 0, 0, 5, 0, 8, 1],
[0, 5, 0, 3, 4, 0, 6, 0, 0],
[4, 0, 2, 0, 0, 0, 0, 0, 0],
[0, 3, 4, 0, 0, 0, 1, 0, 0],
[9, 0, 0, 8, 0, 0, 0, 5, 0],
[0, 0, 0, 4, 0, 0, 3, 0, 7]
]
    empties = 51
    '''

    
    if (empties > 64):
        app.errorBox("Error","There must be atleast 17 cells filled in. Please try again",None)
    else:
        alg(board,empties)        #solves the puzzle

    app.enableButton("Solve")


def createboard():                          #takes all inputs and creates the board
    global empties
    board = []
    empties = 0
    for row in range(0,9):
        rowL = []
        for col in range(0,9):
            input = app.getEntry(str(row)+str(col))
            if input == None:
                input = 0
                empties = empties + 1       #counts empty slots
            rowL.append(input)
        board.append(rowL)
    return board


def validmoves(brd,row,col):                #generates valid numbers to plug into the spot
    valid = [1,2,3,4,5,6,7,8,9]
    for checkrow in range(0,9):
        if (brd[row][checkrow] in valid):        #if the number exists in its row, return false
            valid.remove(brd[row][checkrow])
        
    for checkcol in range(0,9):
        if (brd[checkcol][col] in valid):            #if the number exists in its colum, return false
            valid.remove(brd[checkcol][col])

    boxX = 3* (row//3)   #provides the top left X of its 3x3 box
    boxY = 3 * (col//3)  #provides the top left Y of its 3x3 box
    
    for checkboxX in range(boxX,boxX+3):
        for checkboxY in range(boxY,boxY+3):    #goes through all 9 cells in its 3x3 box
            if (brd[checkboxX][checkboxY] in valid):
                valid.remove(brd[checkboxX][checkboxY])          
    if len(valid) == 0:
        return [0,0,0]           #if there are no valid moves left return 0
    return valid


def validgen(brd2):
    validnums = []
    for row in range(0,9):                      #creates a list of valid moves for each cell
            for col in range(0,9):
                if brd2[row][col] != 0:
                    validnums.append([0,0,0])       #blank list of moves for a cell that already has been filled in (just a filler vector)
                    continue
                validnums.append(validmoves(brd2,row,col))
    return validnums

                
def alg(brd,slots):
    global runtime,limit
    count = 0
    brd2 = copy.deepcopy(brd)
    while (runtime<limit or slots<=count):
        currentempties = count              #saving the current state of count to compare with the post loop results
        for x in range(0,81):                       #iterates through all valid moves
            validnums = validgen(brd2)
            if (validnums[x][0] == 0):
                continue
            if len(validnums[x]) == 1:              #if there is only one solution, plug it into the cell
                row = x//9      
                col = x%9
                brd2[row][col] = validnums[x][0]
                app.setEntry(str(row)+str(col),brd2[row][col],callFunction=False)
                app.setEntryFg(str(row)+str(col),"Green")
                count = count + 1
                continue   
            else:                                 #if there is a possible 2 solutions, find the correct solution
                onlySolution = []
                for test in range(0,len(validnums[x])):
                    found = False
                    row = x//9      
                    col = x%9
                    boxX = 3* (row//3)   #provides the top left X of its 3x3 box
                    boxY = 3 * (col//3)  #provides the top left Y of its 3x3 box
                    indexOfBox = boxY+(boxX*9)
                    boxIndexes = [indexOfBox,indexOfBox+1,indexOfBox+2,indexOfBox+9,indexOfBox+10,indexOfBox+11,indexOfBox+18,indexOfBox+19,indexOfBox+20]  #indexes for the box so I can access the list of valid moves for each cell
                    for indexs in boxIndexes:                                                   #go through all valid moves in the 3x3 of the cell
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):       #if the current number we are testing out of the valid moves are found in another cell,
                            found = True                                                        #that means that number is not a solution for our cell in its 3x3 (nonet)
                            continue                                                            #by finding the number that is unique (not found in the valid moves of its 3x3), that number MUST be the solution to that cell
                    if found == False:   #number isnt found in surrounding 3x3, number MUST be the solution
                        brd2[row][col] = validnums[x][test]
                        app.setEntry(str(row)+str(col),brd2[row][col],callFunction=False)
                        app.setEntryFg(str(row)+str(col),"Green")
                        count = count + 1
                        continue
                    
                    found = False
                    
                    indexOfRow = row*9   #we want to continue trying, now onto row elimination instead of 3x3
                    rowIndexes = [indexOfRow,indexOfRow+1,indexOfRow+2,indexOfRow+3,indexOfRow+4,indexOfRow+5,indexOfRow+6,indexOfRow+7,indexOfRow+8]           #check row if its the only option left
                    for indexs in rowIndexes:
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):
                            found = True                                                        
                            continue                                                            
                    if found == False:                          #number is found in its row, ignore that number
                        brd2[row][col] = validnums[x][test]     #number is unique, set it to its cell
                        app.setEntry(str(row)+str(col),brd2[row][col],callFunction=False)
                        app.setEntryFg(str(row)+str(col),"Green")
                        count = count + 1
                        continue

                    found = False
                    
                    indexOfCol = col
                    colIndexes = [indexOfCol,indexOfCol+1*9,indexOfCol+2*9,indexOfCol+3*9,indexOfCol+4*9,indexOfCol+5*9,indexOfCol+6*9,indexOfCol+7*9,indexOfCol+8*9]       #check col if its the only option left
                    for indexs in colIndexes:
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):
                            found = True                                                        
                            continue                                                            
                    if found == False:                          #number is found in its col, ignore that number
                        brd2[row][col] = validnums[x][test]     #number is unique, set it to its cell
                        app.setEntry(str(row)+str(col),brd2[row][col],callFunction=False)
                        app.setEntryFg(str(row)+str(col),"Green")
                        count = count + 1
                        continue

        if solved(brd2):  #check if the board is solved
            break
                
        if (currentempties == count):    #if no changes have occured after going through 81 cells, it means it is stuck
            nextslot = []
            nextslotindex = 0
            for x in range(0,81):
                if validnums[x][0] != 0:
                    nextslot = validnums[x]     #if the cell is not a filled cell, set the nextslot its valid moves
                    nextslotindex = x
            if nextslot == []:  #if there isnt a cell with valid moves left
                if oldboards.isEmpty():
                    app.errorBox("Error","The program has failed to solve the puzzle",None)
                    runtime = 0
                    app.setMeter("Status",0.0,"Idle")
                    break
                brd2 = oldboards.pop()   #else, try the next board in the stack
            else:   #we have a list of valid moves to fill the cell with
                for y in nextslot:
                    tempbrd = copy.deepcopy(brd2)
                    row = nextslotindex//9      
                    col = nextslotindex%9
                    tempbrd[row][col] = y   #plugging in the number in valid moves
                    oldboards.push(tempbrd)
                brd2 = oldboards.pop()      #get the next board state
            fillboard(brd2)


                        
        app.setMeter("Status",(count/slots)*100,"Solving")
        runtime = runtime + 1
        
    if runtime>=limit:
        app.errorBox("Error","The runtime of the algorithm has exceeded the set limit of "+str(limit),None)
        runtime = 0
        app.setMeter("Status",0.0,"Idle")
    else:
        fillboard(brd2)


def fillboard(brd):
    for row in range(0,9):
        for col in range (0,9):
            if (app.getEntry(str(row)+str(col)) == None):
                app.setEntry(str(row)+str(col),brd[row][col],callFunction=False)
                app.setEntryFg(str(row)+str(col),"Green")
    app.setMeter("Status",0.0,"Idle")

def solved(brd2):
    for row in range(0,9):
        for col in range (0,9):
            if brd2[row][col] == 0:
                return False
    return True


def autosolve(button):
    emptyboard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = time.time()


    app.disableButton("Auto Solve")
    app.disableButton("Solve")
    app.disableButton("Clear")

    hard =app.getEntry("numhard")
    medium = app.getEntry("nummedium")
    easy = app.getEntry("numeasy")
        
    if not isinstance(hard,float):
        hard = 0
    if not isinstance(medium,float):
        medium = 0
    if not isinstance(easy,float):
        easy = 0
    
    for num in range(0,int(hard)):
        cells = sudoparser.parsePuzzle(3)
        temp = copy.deepcopy(emptyboard)
        for cell in cells:
            temp[int(cell[0])][int(cell[1])] = int(cell[2])
        alg(temp,81-len(cells))

        

    for num in range(0,int(medium)):
        cells = sudoparser.parsePuzzle(2)
        temp = copy.deepcopy(emptyboard)
        for cell in cells:
            temp[int(cell[0])][int(cell[1])] = int(cell[2])
        alg(temp,81-len(cells))


            

    for num in range(0,int(easy)):
        cells = sudoparser.parsePuzzle(1)
        temp = copy.deepcopy(emptyboard)
        for cell in cells:
            temp[int(cell[0])][int(cell[1])] = int(cell[2])
        alg(temp,81-len(cells))


   

    

    
        

    app.enableButton("Auto Solve")
    app.enableButton("Solve")
    app.enableButton("Clear")
    
    end = time.time()
    totaltime = end - start
    app.infoBox("Results",str(hard+medium+easy) + " puzzles have been solved in " + str(totaltime) + " seconds.")
    app.clearAllEntries()
    

# create a GUI variable called app
app = gui("Sudoku Solver", "400x450")
app.setLocation("CENTER",y=None)
app.setResizable(canResize=False)
app.setGuiPadding(10, 10)
app.setBg("gray")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later


app.startTabbedFrame("TabbedFrame")

#board tab
app.startTab("Board")
app.startFrame("NONE",row=0,column=0)


for row in range(0,9):
    for col in range (0,9):
        
        app.addNumericEntry(str(row)+str(col),row,col,0,0,False)
        app.setEntryMaxLength(str(row)+str(col),1)
        app.setEntryRelief(str(row)+str(col),"sunken")
        if ((col<=2 or col >= 6) and (row <=2 or row >= 6)) or (row>=3 and row <=5 and col>=3 and col <= 5):
            app.setEntryBg(str(row)+str(col),"light grey")


        


app.stopFrame()

app.addButtons(["Clear","Solve"],[clear,solve])
app.addMeter("Status")


app.stopTab()

app.startTab("Auto")

app.addMessage("auto","""This service will parse online puzzles from http://www.cs.utep.edu/cheon/ws/sudoku/ and solve them""")
app.getMessageWidget("auto").config(font="Helvetica 12 ")
app.setMessageWidth("auto", 350)


app.addNumericEntry("numhard")
app.addNumericEntry("nummedium")
app.addNumericEntry("numeasy")
app.setEntryDefault("numhard","Number of hard puzzles")
app.setEntryDefault("nummedium","Number of medium puzzles")
app.setEntryDefault("numeasy","Number of easy puzzles")

app.addButton("Auto Solve",autosolve)

app.stopTab()



#about tab
app.startTab("About")
app.addMessage("about","Created by Felix Siu")

# start the GUI

app.stopTabbedFrame()
app.go()
