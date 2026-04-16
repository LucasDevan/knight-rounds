from random import shuffle;

continue_to_play=True

def initialiseBoard(board):
        for row in range(size):
            board.append([])
            for  squares in range(size):
                board[row].append(0)
                
                
def numberOfSpaceCanMoveTo(column,row,boardSize):
    countPossibleMovement=0
    if(column+2<boardSize):
        if(row+1<boardSize):
            countPossibleMovement+=1
        if(row-1>=0):
            countPossibleMovement+=1
    if(column-2>0):
        if(row+1<boardSize):
            countPossibleMovement+=1
        if(row-1>=0):
            countPossibleMovement+=1
    if(row-2>0):
        if(column+1<boardSize):
            countPossibleMovement+=1
        if(column-1>=0):
            countPossibleMovement+=1
    if(row+2<boardSize):
        if(column+1<boardSize):
            countPossibleMovement+=1
        if(column-1>=0):
            countPossibleMovement+=1
    return countPossibleMovement


def hamiltonGraphMaker(board):
    hamiltonGraph = []
    countPossibleMovement = 0
    for column in range(len(board)):
            hamiltonGraph.append([])
            for row in range(len(board[column])):
                #print(column,";",row)
                countPossibleMovement=numberOfSpaceCanMoveTo(column,row,len(board))
                #print(countPossibleMovement)
                hamiltonGraph[column].append(countPossibleMovement)
    return  hamiltonGraph

def updatingHamiltonGraph(startingColumn,startingRow,hamiltonGraph):
    hamiltonGraph[startingColumn][startingRow]=-1
    boardSize=len(hamiltonGraph)
    listOfSpaces=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    for space in listOfSpaces:
        currentColumn=startingColumn+space[0]
        currentRow=startingRow+space[1]
        if(currentColumn<boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            if(hamiltonGraph[currentColumn][currentRow]>0):
                hamiltonGraph[currentColumn][currentRow]+=-1

def selectingNextSpace(hamiltongraph,startingColumn=0,startingRow=0):
    boardSize=len(hamiltongraph)
    minValue=10 #Higher then max value in the graph (6)
    newColumn,newRow=-1,-1
    listOfSpaces=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    shuffle(listOfSpaces)
    for space in listOfSpaces:
        currentColumn=startingColumn+space[0]
        currentRow=startingRow+space[1]
        #print("currentColumn: ",currentColumn,"currentRow: ",currentRow," value:",hamiltongraph[currentColumn][currentRow])
        if(currentColumn<boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            if(hamiltongraph[currentColumn][currentRow]>0):
                minValue=hamiltongraph[currentColumn][currentRow]
                newColumn=currentColumn
                newRow=currentRow
    if(newColumn==-1):
        return (-1,-1)
    return (newColumn,newRow)

def solvingForOne(hamiltongraph,listOfMoves,column=0,row=0):
    listOfMoves=[]
    #listOfMoves=['('+(str(column)+";"+str(row))+')']
    while(column!=-1):
        #printBoard(hamiltongraph)
        updatingHamiltonGraph(column,row,hamiltongraph)
        #print(column,";",row," ",board[column][row]," ",hamiltongraph[column][row])
        listOfMoves.append('('+str(column)+";"+str(row)+')')
        #printBoard(hamiltongraph)
        currentspace=selectingNextSpace(hamiltongraph,column,row)
        column=currentspace[0]
        row=currentspace[1]

    return listOfMoves

def solving(board,column=0,row=0):
    listOfMoves=[(0,0)]
    while(len(listOfMoves)<len(board)*len(board)):
        hamiltongraph=hamiltonGraphMaker(board)
        listOfMoves=solvingForOne(hamiltongraph,column,row)
        #print(len(board)*len(board)," ",len(listOfMoves)," listOfMoves ",listOfMoves)
        print(len(board)*len(board)," ",len(listOfMoves))
    print(len(board)*len(board)," ",len(listOfMoves)," listOfMoves ",listOfMoves)
    printBoard(hamiltongraph)
    return listOfMoves

def printBoard(board):
    for elements in range(len(board)*2+1):
        print("-",end="")
    print("")
    for row in board:
        print("",end="|")
        for  squares in row:
            print(squares,end="|")
        print()
        for elements in range(len(row)*2+1):
            print("-",end="")
        print("")


while(continue_to_play):
    print("Rentrer la taille d'échequier voulue :")
    size = int(input(""))
    if(size==1):
        print("La solution est: [(0,0)]")
    elif(size<=4):
        print("La taille renter ne permetre pas de résoudre le problème.")
    else:
        board = []
        listOfMoves = []
        initialiseBoard(board)
        listOfMoves=solving(board)
        if(len(listOfMoves)<size*size):
            print("pas de solution trouvez")
        else:
            print("Une des solutions est:")
        print(listOfMoves)
    print("Voulez-vous recommencer?  (Oui ou Non)")
    choix=str(input(""))
    if(choix.lower()=="non"):
        continue_to_play=False
print("Aurevoire !")
            
    
    