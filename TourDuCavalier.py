knightsMovements=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] #Liste des mouvements possibles du cavalier en coordonnées relatives.
continue_to_play=True #Booléen contrôlant la répétition du programme.

def initialiseBoard(board:list, boardSize:int)->list:
    """_summary_
        Initialise un échiquier vide en remplissant une liste avec des zéros.
    Args:
        board (list): liste vide qui représentera l'échiquier
    """
    for row in range(boardSize):
        board.append([0]*boardSize)

def numberOfSpaceCanMoveTo(startingColumn:int,startingRow:int,boardSize:int)->int:
    """_summary_
    Calcule le nombre de cases valides accessibles depuis une position donnée.
    Args:
        startingColumn (int):  Colonne de départ.
        startingRow (int):  Ligne de départ.
        boardSize (int): Taille de l'échiquier.

    Returns:
        countPossibleMovement int: Nombre de mouvements possibles.
    """
    global knightsMovements
    countPossibleMovement : int = 0
    for space in knightsMovements:
        currentColumn = startingColumn + space[0]
        currentRow = startingRow + space[1]
        if(currentColumn < boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            countPossibleMovement += 1
    return countPossibleMovement

def hamiltonGraphMaker(board:list)->list:
    """_summary_
    Construit une graph hamiltonnien indiquant le nombre de déplacements possibles pour chaque case.
    Args:
        board (list): La liste qui représentera l'échiquier.

    Returns:
        list: le graph hamiltonnien des déplacements possible du cavalier sur l'échiquier
    """
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

def updatingHamiltonGraph(startingColumn:int,startingRow:int,hamiltonGraph:list,Update:bool):
    """_summary_
    Met à jour la matrice de graphes hamiltoniens après le passage du cavalier.
    Args:
        startingColumn (int): Colonne actuelle.
        startingRow (int): Ligne actuelle.
        hamiltonGraph (list): graph hamiltonnien des déplacements possible du cavalier
        Update (bool): Indique si on ajoute ou enlève un mouvement possible
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
    """_summary_
    Renvoie les mouvements valides triés par ordre croissant du nombre de possibilités restantes.
    Args:
        column (int): Colonne actuelle
        row (int): Ligne actuelle
        hamiltongraph (list): graph hamiltonnien des déplacements possible du cavalier
        boardSize (int): Taille de l'échiquier.

    Returns:
        list: Liste des mouvements classés par priorité.
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

def solving(boardSize:int,listOfMoves:list,hamiltongraph:list,column:int,row:int)->tuple:
    """_summary_
    Résout le problème du tour du cavalier en utilisant une approche récursive avec l'algorithme de résolution rapide bassé sur la recherche du meilleur coût à chaque tour
    
    Args:
        boardSize (int): Taille de l'échiquier
        listOfMoves (list): Liste des mouvements effectués
        hamiltongraph (list): Matrice des mouvements possibles
        column (int): Colonne actuelle
        row (int): Ligne actuelle

    Returns:
        tuple(bool, list): Statut de réussite et liste des mouvements déjà effectuer
    """
    updatingHamiltonGraph(column,row,hamiltongraph,True)
    listOfMoves.append((column,row))
    #print(len(listOfMoves))
    if(len(listOfMoves)==boardSize*boardSize):
        return (True,listOfMoves)
    priorityMoves=getPriorityMoves(column,row,hamiltongraph,boardSize)
    for move in priorityMoves:
        if(move[0]>=0):
            result = solving(boardSize,listOfMoves,hamiltongraph,move[1],move[2])
            if(result[0]):
                return result
            listOfMoves.remove((move[1],move[2]))
            updatingHamiltonGraph(move[1],move[2],hamiltongraph,False)
    return (False,[])

def solverChecker(listOfMoves:list,boardSize:int)->bool:
    """_summary_
    Vérifie si la solution trouvée couvre bien toutes les cases de l'échiquier un seull foi.
    Args:
        listOfMoves (list): Liste des déplacements du cavalier.
        boardSize (int): Taille de l'échiquier.

    Returns:
        bool: Indique si la solution est correcte.
    """
    try:
        for i in range(0,boardSize):
            for j in range(0,boardSize):
                    listOfMoves.remove((i,j))
    except:
        print("Un des coups n'est pas dans la liste")
        return False
    if(len(listOfMoves)==0):
        return True
    return False

def printBoard(board:list):
    """_summary_
    Affiche l'échiquier (ou graph) sous forme textuelle.
    Args:
        board (list): L'échiquier (ou graph) à afficher.
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

print("Bienvenue dans le jeu du tour du cavalier!")
print("Dans ce jeu, un cavalier doit parcourir toutes les cases d'un échiquier sans repasser par la même deux fois!")
print("Ce programme va automatiquement résoudre ce tour avant d'afficher la liste des mouvements effectués par le cavalier"+'\n')

INVALIDE_SIZE_VALUE : int = -1
MIN_BOARD_SIZE : int = 1
UNSOLVABLE_SIZES : list = [2,3]
MAX_BOARD_SIZE : int = 31

DEFAULT_POSITION : int = 0

boardSizeInput : str
rowPositionInput : str
lignePositionInput : str

boardSize : int
rowPosition : int
lignePosition : int

board : list

while(continue_to_play):
    rowPosition = INVALIDE_SIZE_VALUE # reset the values on start
    lignePosition = INVALIDE_SIZE_VALUE # reset the values on start

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
        while(rowPosition < 0 or rowPosition>=boardSize):#test si la valeur rentrée est correct
            try:
                rowPositionInput = input(f"Rentrer la colonne de 0 à {boardSize-1} sur laquelle le cavalier vas commencer son tour: ") #Position initiale en colonne
                rowPosition = int(rowPositionInput)
            except:
                print("Vous avez rentré une valeur non conforme, la colonne de départ sera la ",DEFAULT_POSITION)
                rowPosition = DEFAULT_POSITION

        while(lignePosition < 0 or lignePosition>=boardSize):#test si la valeur rentrée est correct
            try:
                lignePositionInput = input(f"Rentrer la ligne de 0 à {boardSize-1} sur laquelle le cavalier va commencer son tour: ") #Position initiale en ligne
                lignePosition = int(lignePositionInput)
            except:
                print("Vous avez rentré une valeur non conforme, la ligne de départ sera la ",DEFAULT_POSITION)
                lignePosition = DEFAULT_POSITION
        print("")
        input(f"Tout est prêt! Appuyez sur Entrée pour générer la solution au problème du tour du cavalier sur un plateau de {boardSize} par {boardSize} avec la position de départ à la case ({rowPosition},{lignePosition}) ")

        board = []
        initialiseBoard(board,boardSize)
        hamiltongraph = hamiltonGraphMaker(board)
        try:
            result = solving(len(board),[],hamiltongraph,rowPosition,lignePosition)
            copyList = result[1].copy() #La liste des coups est comprit dans res[1]
            if(not result[0] or not solverChecker(copyList,len(board))):
                print("Aucune solution n'a été trouvée pour un échiquier de ",boardSize," par ",boardSize)
            else:
                print("Une des solutions est:",result[1]) #affiche la solution
        except RecursionError:
            print(f"La taille de l'échiquier est trop grande pour que l'algorithme puisse résoudre le tour du cavalier (max:{MAX_BOARD_SIZE})")

    print("Voulez-vous recommencer?  (Tapper 'Non' pour quitter)")
    choix=str(input("")).lower() #Permet de rejouer ou quitter le programme
    if(choix=="non" or choix=="n" or choix=="no"):
        continue_to_play = False
    
print("Au revoire !")