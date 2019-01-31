

# import the library
from appJar import gui

#fields/variables
progress = 0
count = 0



# handle button events
def clear(button):
    global progress
    app.setMeter("Status",99.0,"Working")
    app.clearAllEntries(callFunction=False)
    app.setMeter("Status",0.0,"Idle")
    progress = 0
            

            

def solve(button):
    print("hi")



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
        app.setEntryDefault(str(row)+str(col), "-")
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
