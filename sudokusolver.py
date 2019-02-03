

# import the library
from appJar import gui
from copy import copy

#fields/variables
progress = 0
count = 0
empties = 0
validnums = []
runtime = 0
limit = 1000



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
    grid = [
[4, 0, 0, 0, 0, 5, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 9, 8],
[3, 0, 0, 0, 8, 2, 4, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 8, 0],
[9, 0, 3, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 3, 0, 6, 7, 0],
[0, 5, 0, 0, 0, 9, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 9, 0, 7],
[6, 4, 0, 3, 0, 0, 0, 0, 0],
]
    board = createboard()     #creates a list with all 9 rows based off input
    #if (empties > 64):
       # app.errorBox("Error","There must be atleast 17 cells filled in. Please try again",None)
   # else:
    alg(grid,55)        #solves the puzzle

    


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
        return 0           #if there are no valid moves left return 0
    return valid

def validgen(brd2):
    validnums = []
    for row in range(0,9):                      #creates a list of valid moves for each cell
            for col in range(0,9):
                if brd2[row][col] != 0:
                    validnums.append([0,0,0])       #blank list of moves for a cell that already has been filled in
                    continue
                validnums.append(validmoves(brd2,row,col))
    return validnums
                
def alg(brd,slots):
    global validnums,runtime,limit
    count = 0
    brd2 = copy(brd)
    while ((slots-count) > 0) and (runtime<limit):  
        for x in range(0,81):                       #iterates through all valid moves
            validnums = validgen(brd2)  
            if len(validnums[x]) == 1:              #if there is only one solution, plug it into the cell
                row = x//9      
                col = x%9
                brd2[row][col] = validnums[x][0]
                count = count + 1
                continue
            #elif (len(validnums[x]) == 2):          #if there is a possible 2 solutions, find the correct solution
            else:
                if (validnums[x][0] == 0):
                    continue
                for test in range(0,len(validnums[x])):
                    print(validnums[x])
                    onlySolution = True
                    row = x//9      
                    col = x%9
                    boxX = 3* (row//3)   #provides the top left X of its 3x3 box
                    boxY = 3 * (col//3)  #provides the top left Y of its 3x3 box
                    indexOfBox = boxY+(boxX*9)
                    boxIndexes = [indexOfBox,indexOfBox+1,indexOfBox+2,indexOfBox+9,indexOfBox+10,indexOfBox+11,indexOfBox+18,indexOfBox+19,indexOfBox+20]  #indexes for the box so I can access the list of valid moves for each cell
                    for indexs in boxIndexes:
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):
                            onlySolution = False
                           
                    indexOfRow = row*9
                    rowIndexes = [indexOfRow,indexOfRow+1,indexOfRow+2,indexOfRow+3,indexOfRow+4,indexOfRow+5,indexOfRow+6,indexOfRow+7,indexOfRow+8]           #check row if its the only option left
                    for indexs in rowIndexes:
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):
                            onlySolution = False

                    indexOfCol = col
                    colIndexes = [indexOfCol,indexOfCol+1*9,indexOfCol+2*9,indexOfCol+3*9,indexOfCol+4*9,indexOfCol+5*9,indexOfCol+6*9,indexOfCol+7*9,indexOfCol+8*9]       #check col if its the only option left
                    for indexs in colIndexes:
                        if ((validnums[x][test] in validnums[indexs]) and (x != indexs)):
                            onlySolution = False
                    
                            
                    if onlySolution == True:
                        brd2[row][col] = validnums[x][test]
                        count = count + 1
                        break

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
