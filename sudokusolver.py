

# import the library
from appJar import gui
from copy import copy

#fields/variables
progress = 0
count = 0
empties = 0
validnums = []


# handle button events
def clear(button):
    global progress
    app.setMeter("Status",99.0,"Working")
    app.clearAllEntries(callFunction=False)
    app.setMeter("Status",0.0,"Idle")
    progress = 0
            

            

def solve(button):
    global validnums
    brd = createboard()     #creates a list with all 9 rows based off input
    test1 = [
[4, 7, 0, 0, 0, 0, 0, 5, 0],
[0, 0, 5, 0, 6, 9, 4, 0, 0],
[9, 0, 0, 0, 4, 0, 2, 8, 0],
[0, 5, 0, 0, 3, 0, 8, 2, 4],
[2, 0, 0, 0, 9, 0, 0, 0, 6],
[6, 4, 8, 0, 7, 0, 0, 1, 0],
[0, 2, 7, 0, 1, 0, 0, 0, 8],
[0, 0, 4, 3, 2, 0, 7, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 9, 2]
]


    print(test1)
    brdfinish = alg(test1,empties)        #solves the puzzle
    print(brdfinish)
    


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
    print(valid)           
    if len(valid) == 0:
        return 0           #if there are no valid moves left return 0
    return valid

'''
def alg(brd,slots):
    global validnums
    count = 0
    brd2 = copy(brd)
    while (slots-count) > 0:
        validnums = []
        for row in range(0,9):
            for col in range(0,9):
                if brd2[row][col] != 0:
                    validnums.append([0,0])
                    continue
                validnums.append(validmoves(brd2,row,col))
                
        for x in range(0,81):
            #print(len(validnums[x]))
            if len(validnums[x]) == 1:
                row = x//9      
                col = x%9
                print(validnums[x][0])
                print(row)
                print(col)
                brd2[row][col] = validnums[x][0]
                count = count + 1
                continue
        print(validnums)
    print("Solved")
    return brd2
'''

            

def alg(brd, slots):              #recursive function with backtracking to solve puzzle
    if slots == 0:
        print("solved")
        return True
    for row in range(0,9):
        for col in range(0,9):
            cell = brd[row][col]
            
            if cell != 0:           #so if the cell is occupied jump to next cell
                continue

            valid = validmoves(brd,row,col)

            
            if valid == 0:
                return False
            for testing in valid:
                brd[row][col] = testing
                if alg(brd,slots-1):
                    return True
                brd[row][col] = 0
                


#def solved?(board):
#
#    for checkrow in range(0,9):
#        used = []
#        for checkcol in range(0,9):
#            if (brd[checkrow][checkcol] in used):        #if the number reoccurs again in its row, return false
#                return false
#            else:
#                used.append(brd[checkrow][checkcol])
#
#    for checkcol in range(0,9):
#        used = []
#        for checkrow in range(0,9):
#            if (brd[checkrow][checkcol] in used):        #if the number reoccurs again in its row, return false
#                return false
 #           else:
#                used.append(brd[checkrow][checkcol])

##    for boxX in range(
#    for checkboxX in range(boxX,boxX+3):
 #       for checkboxY in range(boxY,boxY+3):    #goes through all 9 cells in its 3x3 box
 #           if (brd[checkboxX][checkboxY] in valid):
 #               valid.remove(brd[checkboxX][checkboxY])


                
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
