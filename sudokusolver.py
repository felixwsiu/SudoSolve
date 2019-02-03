

# import the library
from appJar import gui
from copy import copy

#fields/variables
progress = 0
count = 0
empties = 0
runtime = 0
limit = 500



# handle button events
def clear(button):
    clearboard()
            
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
    
    board = createboard()     #creates a list with all 9 rows based off input
    if (empties > 64):
        app.errorBox("Error","There must be atleast 17 cells filled in. Please try again",None)
    else:
        alg(board,empties)        #solves the puzzle

    


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
    brd2 = copy(brd)
    while (runtime<limit):
        if slots <= count:
            break
        for x in range(0,81):                       #iterates through all valid moves
            validnums = validgen(brd2)
            if (validnums[x][0] == 0):
                continue
            if len(validnums[x]) == 1:              #if there is only one solution, plug it into the cell
                row = x//9      
                col = x%9
                brd2[row][col] = validnums[x][0]
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
                    if found == True:   #number is found in surrounding 3x3, ignore that number
                        continue
                    else:
                        brd2[row][col] = validnums[x][test] #number isn't found and unique, set it to its cell
                        count = count + 1
                    
        app.setMeter("Status",(count/slots)*100,"Solving")
        runtime = runtime + 1
        
    if runtime>=limit:
        app.errorBox("Error","The runtime of the algorithm has exceeded the set limit of "+str(limit),None)
        clearboard()
    else:
        fillboard(brd2)

def fillboard(brd):
    for row in range(0,9):
        for col in range (0,9):
            if (app.getEntry(str(row)+str(col)) == None):
                app.setEntry(str(row)+str(col),brd[row][col],callFunction=False)
                app.setEntryFg(str(row)+str(col),"Green")
    app.setMeter("Status",0.0,"Idle")




       
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


#about tab
app.startTab("About")

app.stopTab()


# start the GUI

app.stopTabbedFrame()
app.go()
