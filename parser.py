import requests
from bs4 import BeautifulSoup

def parsePuzzle(difficulty):
    if difficulty == 3:
        URL = "http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=3"
    elif difficulty == 2:
        URL = "http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=2"
    elif difficulty == 1:
        URL = "http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=1"
        
    r = requests.get(URL)

    soup = BeautifulSoup(r.content,'html5lib')
    soup.prettify()

    info=[]  # a list to store quotes 

    info = soup.find('body').get_text()

    info = info.split('{')

    cells = []

    for x in info:
        text = list(x)
        if len(text) < 24 and len(text)!=0:
            cells.append([text[4],text[10],text[20]])
    print(cells)
    return cells
