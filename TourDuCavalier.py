knightsMovements=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] #Liste des mouvements possibles du cavalier en coordonnées relatives.
continue_to_play=True #Booléen contrôlant la répétition du programme.

def initialiseBoard(board:list)->list:
    """_summary_
        Initialise un échiquier vide en remplissant une liste avec des zéros.
    Args:
        board (list): liste vide qui représentera l'échiquier
    """
    for row in range(size):
        board.append([0]*size)
                
                
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
    countPossibleMovement=0
    for space in knightsMovements:
        currentColumn=startingColumn+space[0]
        currentRow=startingRow+space[1]
        if(currentColumn<boardSize and currentColumn>=0 and currentRow>=0 and currentRow<boardSize):
            countPossibleMovement+=1
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
            res=solving(boardSize,listOfMoves,hamiltongraph,move[1],move[2])
            if(res[0]):
                return (True,res[1])
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

print("Bienvenue dans le jeu du tour du cavalier!",end="")
print("Dans ce jeu, un cavalier doit parcourir toutes les cases d'un échiquier sans repasser par la même deux fois!",end="")
print("Ce programme va automatiquement résoudre ce tour avant d'afficher la liste des mouvements effectués par le cavalier")
while(continue_to_play):
    try:
        size=input("Rentrer la taille d'échiquier que le cavalier va parcourir: ") #Taille de l'échiquier
        size = int(size)
    except:
        size='e' #valeur en cas d'exception 
    try:
        colonne=input(f"Rentrer la position de base du cavalier sur les colonnes de 0 à {size-1} (le défaut sera 0): ") #Position initiale en colonne
        colonne = int(colonne)
        ligne=input(f"Rentrer la position de base du cavalier sur les lignes de 0 à{size-1} (le défaut sera 0): ") #Position initiale en ligne
        ligne = int(ligne)
    except:
        size='e'#valeur en cas d'exception 
        
            
    if(size=='e'): #teste si il y a eu une exception
        print("Aille vous n'avez pas rentré un nombre entier strictement positif, veuillez réessayer!") 
    elif(size==1):
        print("La solution est: [(0,0)]") #Solution trivial
    elif(size<=3):
        print("La taille rentrée ne permet pas de résoudre le problème.") #Impossible à réssoudre donc aucun intéret a faire les calcules
    else:
        if(colonne<0 or colonne>=size): #test si la valeur rentrée est correct
            colonne=0 
        if(ligne<0 or ligne>=size): #test si la valeur rentrée est correct
            ligne=0    
        board = []
        initialiseBoard(board)
        hamiltongraph=hamiltonGraphMaker(board)
        try:
            res=solving(len(board),[],hamiltongraph,colonne,ligne)
            copyList=res[1].copy() #La liste des coups est comprit dans res[1]
            if(not res[0] or not solverChecker(copyList,len(board))):
                print("pas de solution trouvez")
            else:
                print("Une des solutions est:",res[1]) #affiche la solution
        except RecursionError:
            print("La taille que vous avez rentrée est trop grande pour que Python puisse résoudre (max:31)")

    print("Voulez-vous recommencer?  (Oui ou Non)")
    choix=str(input("")) #Permet de rejouer ou quitter le programme
    if(choix.lower()=="non"):
        continue_to_play=False
    
print("Au revoire !")