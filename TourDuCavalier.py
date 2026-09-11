import sys

knightsMovements=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] #Liste des mouvements possibles du cavalier en coordonnées relatives.

INVALIDE_SIZE_VALUE : int = -1
MIN_BOARD_SIZE : int = 1
UNSOLVABLE_SIZES : list = [2,3]
MAX_BOARD_SIZE : int = 31

DEFAULT_POSITION : int = 0

class ListOfMoves:
    def __init__(self,listOfMoves:list | None = None):
        """Create a move list, optionally initialized with existing moves."""
        self.__list_of_moves : list = [] if listOfMoves is None else listOfMoves
        self.__is_solution : bool = False

    def addMove(self,columnPosition: int, rowPosition:int):
        """Add a board position to the end of the move list.

        Args:
            columnPosition: The column of the move.
            rowPosition: The row of the move.
        """
        self.__list_of_moves.append((columnPosition,rowPosition))

    def removeMove(self,columnPosition: int, rowPosition:int):
        """Remove a board position from the move list if it is present.

        Args:
            columnPosition: The column of the move.
            rowPosition: The row of the move.
        """
        if(len(self.__list_of_moves)==0):
            return
        try:
            self.__list_of_moves.remove((columnPosition,rowPosition))
        except:
            print("Move not in list")

    def getNumberOfMoves(self)->int:
        """Return the number of moves currently stored."""
        return len(self.__list_of_moves)

    def getListOfMoves(self)->list:
        """Return the list of stored board positions."""
        return self.__list_of_moves

    def isListOfMovesFull(self,boardSize:int)->bool:
        """Return whether the list contains one move for every board square.

        Args:
            boardSize: The length of one side of the square board.
        """
        return len(self.__list_of_moves) == boardSize*boardSize

    def isSolution(self,boardSize:int)->bool:
        """Return whether the moves cover every board square exactly once.

        Args:
            boardSize: The length of one side of the square board.

        Returns:
            True if the move list is a valid knight's tour, otherwise False.
        """
        if(self.__is_solution == True):
            return True
        
        if(not self.isListOfMovesFull(boardSize)):
            return False

        copyList = self.__list_of_moves.copy()

        try:
            for i in range(0,boardSize):
                for j in range(0,boardSize):
                    copyList.remove((i,j))
        except:
            print("Un des coups n'est pas dans la liste")
            self.__is_solution = False
            return False
        if(len(copyList)==0):
            self.__is_solution = True
        else:
            self.__is_solution = False
        return self.__is_solution
    
def numberOfSpaceCanMoveTo(startingColumn:int,startingRow:int,boardSize:int)->int:
    """Count the valid board squares reachable from a position.

    Args:
        startingColumn: The starting column.
        startingRow: The starting row.
        boardSize: The length of one side of the square board.

    Returns:
        The number of valid knight moves from the starting position.
    """
    global knightsMovements
    countPossibleMovement : int = 0
    for space in knightsMovements:
        currentColumn = startingColumn + space[0]
        currentRow = startingRow + space[1]
        if(currentColumn < boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            countPossibleMovement += 1
    return countPossibleMovement


def initialiseBoard(board:list, boardSize:int)->list:
    """Fill a board list with empty rows initialized to zero.

    Args:
        board: The list that will represent the board.
        boardSize: The length of one side of the square board.
    """
    for row in range(boardSize):
        board.append([0]*boardSize)


def hamiltonGraphMaker(boardSize:int)->list:
    """Build a graph containing the available moves for every board square.

    Args:
        boardSize: The length of one side of the square board.

    Returns:
        A matrix containing the number of possible knight moves for each square.
    """
    hamiltonGraph = []
    countPossibleMovement = 0
    for column in range(boardSize):
        hamiltonGraph.append([])
        for row in range(boardSize):
            #print(column,";",row)
            countPossibleMovement=numberOfSpaceCanMoveTo(column,row,boardSize)
            #print(countPossibleMovement)
            hamiltonGraph[column].append(countPossibleMovement)
    return  hamiltonGraph

def updatingHamiltonGraph(startingColumn:int,startingRow:int,hamiltonGraph:list,Update:bool):
    """Update move counts after visiting or backtracking from a square.

    Args:
        startingColumn: The column of the current square.
        startingRow: The row of the current square.
        hamiltonGraph: The matrix of remaining move counts.
        Update: If True, mark the square visited and decrease neighboring counts;
            otherwise, restore the square and increase neighboring counts.
    """
    global knightsMovements
    if(Update): #Si on update, on met la case courante à -1
        hamiltonGraph[startingColumn][startingRow]=-1
    else: #Si on un-update, on met la case courante à 1 pour pouvoir y re-accéder
        hamiltonGraph[startingColumn][startingRow]=1
    boardSize=len(hamiltonGraph)
    for space in knightsMovements:
        currentColumn=startingColumn+space[0]
        currentRow=startingRow+space[1]
        if(currentColumn<boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            if(hamiltonGraph[currentColumn][currentRow]>0):
                if(Update):
                    #print("Update")
                    hamiltonGraph[currentColumn][currentRow]-=1
                else:
                    #print("NO Update")
                    hamiltonGraph[currentColumn][currentRow]+=1
                    
                    
def getPriorityMoves(column:int,row:int,hamiltongraph:list,boardSize:int)->list:
    """Return valid next moves sorted by remaining move count.

    Args:
        column: The current column.
        row: The current row.
        hamiltongraph: The matrix of remaining move counts.
        boardSize: The length of one side of the square board.

    Returns:
        A list of moves ordered from fewest to most remaining options.
    """
    global knightsMovements
    priorityMoves=[]
    for space in knightsMovements:
        currentColumn=column+space[0]
        currentRow=row+space[1]
        if(currentColumn<boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            priorityMoves.append((hamiltongraph[currentColumn][currentRow],currentColumn,currentRow))
            priorityMoves.sort()
    return priorityMoves

def solving(boardSize:int,hamiltongraph:list,column:int,row:int,listOfMoves:ListOfMoves | None = None)->ListOfMoves:
    """Solve the knight's tour using recursive Warnsdorff-style backtracking.

    The next square is selected according to the number of remaining moves,
    prioritizing squares with fewer available options.
    
    Args:
        boardSize: The length of one side of the square board.
        hamiltongraph: The matrix of remaining move counts.
        column: The current column.
        row: The current row.
        listOfMoves: The moves already made, or None to start a new solution.

    Returns:
        The completed solution, or an empty move list if no solution is found.
    """
    if listOfMoves is None:
        listOfMoves = ListOfMoves()
    updatingHamiltonGraph(column,row,hamiltongraph,True)
    listOfMoves.addMove(column,row)
    #print(len(currentBoardState))
    if(listOfMoves.isSolution(boardSize)):
        return listOfMoves
    priorityMoves : list = getPriorityMoves(column,row,hamiltongraph,boardSize)
    for move in priorityMoves:
        if(move[0]>=0):
            listOfMoves : ListOfMoves = solving(boardSize,hamiltongraph,move[1],move[2],listOfMoves)
            if(listOfMoves.isSolution(boardSize)):
                return listOfMoves
            listOfMoves.removeMove(move[1],move[2])
            updatingHamiltonGraph(move[1],move[2],hamiltongraph,False)
    return ListOfMoves([])

def setUpAndSolves(boardSize:int,columnPosition:int,rowPosition:int)->str:
    if(boardSize < MIN_BOARD_SIZE or boardSize >MAX_BOARD_SIZE):
        return f"Invalide size, please input a value strictly between {MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}"
    elif(boardSize in UNSOLVABLE_SIZES):
        return f"No solution for a board of size {boardSize} by {boardSize}"
    elif(boardSize == MIN_BOARD_SIZE):
        return "[(0,0)]"

    if(columnPosition < 0 or columnPosition>=boardSize):#test si la valeur rentrée est correct
        columnPosition = DEFAULT_POSITION

    if(rowPosition < 0 or rowPosition>=boardSize):#test si la valeur rentrée est correct
        rowPosition = DEFAULT_POSITION

    hamiltongraph = hamiltonGraphMaker(boardSize)
    resultListOfMoves = ListOfMoves()
    solvedMoves = solving(boardSize,hamiltongraph,columnPosition,rowPosition,resultListOfMoves)

    if(solvedMoves.isSolution(boardSize)):
        return str(solvedMoves.getListOfMoves())

    return f"No solution found for a {boardSize} by {boardSize} board starting from {columnPosition,rowPosition}"

def printBoard(board:list):
    """Print a board or move graph in a simple text-based format.

    Args:
        board: The board or graph to print.
    """
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

def main():
    print("Bienvenue dans le jeu du tour du cavalier!")
    print("Dans ce jeu, un cavalier doit parcourir toutes les cases d'un échiquier sans repasser par la même deux fois!")
    print("Ce programme va automatiquement résoudre ce tour avant d'afficher la liste des mouvements effectués par le cavalier"+'\n')

    boardSizeInput : str
    columnPositionInput : str
    rowPositionInput : str

    boardSize : int
    columnPosition : int
    rowPosition : int

    continue_to_play : bool =True #Booléen contrôlant la répétition du programme.

    resultListOfMoves : ListOfMoves

    while(continue_to_play):
        columnPosition = INVALIDE_SIZE_VALUE # reset the values on start
        rowPosition = INVALIDE_SIZE_VALUE # reset the values on start
        resultListOfMoves = ListOfMoves()

        try:
            boardSizeInput = input("Rentrer la taille de l'échiquier que le cavalier va parcourir (par exemple: 5 pour 5X5): ") #Taille de l'échiquier
            boardSize = int(boardSizeInput)
        except:
            boardSize = INVALIDE_SIZE_VALUE #valeur en cas d'exception 

        print("")
        if(boardSize == INVALIDE_SIZE_VALUE or boardSize < MIN_BOARD_SIZE): #teste si il y a eu une exception
            print("Aille vous n'avez pas rentré un nombre entier strictement positif, veuillez réessayer!") 
        elif(boardSize == MIN_BOARD_SIZE):
            print("La solution est: [(0,0)]") #Solution trivial
        elif(boardSize in UNSOLVABLE_SIZES):
            print("L'échiquier est trop petit pour résoudre le problème.") #Impossible à réssoudre donc aucun intéret a faire les calcules
        elif(boardSize > MAX_BOARD_SIZE):
            print(f"La taille d'échéquier que vous avez rentrée est trop grande pour que l'algorithme puisse le résoudre (max:{MAX_BOARD_SIZE})")
        else:
            while(columnPosition < 0 or columnPosition>=boardSize):#test si la valeur rentrée est correct
                try:
                    columnPositionInput = input(f"Rentrer la colonne de 0 à {boardSize-1} sur laquelle le cavalier vas commencer son tour: ") #Position initiale en colonne
                    columnPosition = int(columnPositionInput)
                except:
                    print("Vous avez rentré une valeur non conforme, la colonne de départ sera la ",DEFAULT_POSITION)
                    columnPosition = DEFAULT_POSITION

            while(rowPosition < 0 or rowPosition>=boardSize):#test si la valeur rentrée est correct
                try:
                    rowPositionInput = input(f"Rentrer la ligne de 0 à {boardSize-1} sur laquelle le cavalier va commencer son tour: ") #Position initiale en ligne
                    rowPosition = int(rowPositionInput)
                except:
                    print("Vous avez rentré une valeur non conforme, la ligne de départ sera la ",DEFAULT_POSITION)
                    rowPosition = DEFAULT_POSITION
            print("")
            input(f"Tout est prêt! Appuyez sur Entrée pour générer la solution au problème du tour du cavalier sur un plateau de {boardSize} par {boardSize} avec la position de départ à la case ({columnPosition},{rowPosition}) ")

            hamiltongraph = hamiltonGraphMaker(boardSize)
            try:
                resultListOfMoves = solving(boardSize,hamiltongraph,columnPosition,rowPosition,resultListOfMoves)

                if(resultListOfMoves.isSolution(boardSize)):
                    print("Une des solutions est:",resultListOfMoves.getListOfMoves()) #affiche la solution
                else:
                    print(f"Aucune solution n'a été trouvée pour un échiquier de {boardSize} par {boardSize} avec la position de départ à la case ({columnPosition},{rowPosition})")
            except RecursionError:
                print(f"La taille de l'échiquier est trop grande pour que l'algorithme puisse résoudre le tour du cavalier (max:{MAX_BOARD_SIZE})")

        print("Voulez-vous recommencer?  (Tapper 'Non' pour quitter)")
        choice = str(input("")).lower() #Permet de rejouer ou quitter le programme
        if(choice=="non" or choice=="n" or choice=="no"):
            continue_to_play = False

    print("Au revoire !")


if __name__ == "__main__" and sys.platform != "emscripten":
    main()