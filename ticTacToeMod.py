import os, shelve



def printBoard(board):
    '''
    Prints the game board and gives the players a visual representation
    of what's happening during gameplay.
    '''
    print('|' + board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'] + '|')
    print('-+-+-+-+-')
    print('|' + board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'] + '|')
    print('-+-+-+-+-')
    print('|' + board['low-L'] + '|' + board['low-M'] + '|' + board['low-R'] + '|')

def check_avail_chars(avail_chars, player_char):
    if avail_chars[player_char] == 0:
        return False
    else:
        return True

def gameCheck(theBoard, char):
    '''
    This checks if a player has characters in a straight line horizontally, 
    vertically or even diagonally.
    Returns True if condition is satisfied.
    False, otherwise
    '''
    if theBoard['top-L'] == char and theBoard['mid-M'] == char and theBoard['mid-M'] == char and theBoard['low-R'] == char:
        return True
    elif theBoard['low-L'] == char and theBoard['mid-M'] == char and theBoard['mid-M'] == char and theBoard['top-R'] == char:
        return True
    elif theBoard['top-L'] == char and theBoard['mid-L'] == char and theBoard['mid-L'] == char and theBoard['low-L'] == char:
        return True
    elif theBoard['top-M'] == char and theBoard['mid-M'] == char and theBoard['mid-M'] == char and theBoard['low-M'] == char:
        return True
    elif theBoard['top-R'] == char and theBoard['mid-R'] == char and theBoard['mid-R'] == char and theBoard['low-R'] == char:
        return True
    elif theBoard['top-L'] == char and theBoard['top-M'] == char and theBoard['top-M'] == char and theBoard['top-R'] == char:
        return True
    elif theBoard['mid-L'] == char and theBoard['mid-M'] == char and theBoard['mid-M'] == char and theBoard['mid-R'] == char:
        return True
    elif theBoard['low-L'] == char and theBoard['low-M'] == char and theBoard['low-M'] == char and theBoard['low-R'] == char:
        return True
    else:
        return False

def getUsersVar(avail_chars):
    player_1 = str.capitalize(input("What is your name? "))
    print(f'Hello {player_1}, which character would you like to choose. "X" or "O"')
    while True:
        player_1_char = str.upper(input())
        if player_1_char not in avail_chars.keys():
            print("Sorry, I did not understand your input. Characters are either 'X' or 'O'")
            print()
        else:
            print(f"{player_1}, your character is {player_1_char}")
            print()
            break
    player_2 = str.capitalize(input("What is your name? "))
    if player_1_char == "X":
        player_2_char = "O"
    else:
        player_2_char = "X"
    print(f"{player_2}, your character is {player_2_char}")
    print()
    return {player_1: player_1_char, player_2: player_2_char}

def gamePlay(theBoard, avail_chars, gamePlayVars):
    print("This is the infamous Tic-Tac-Toe game. Choose a card, either 'X' or 'O'.", end = ' ')
    print("Arrange your characters to form a straight three arrangement, either", end = ' ')
    print("diagonally, horizontally or vertically.", end = '\n')
    print("Remember to counterattack your opponent and be the first to get an arrangement!!")
    print()
    
    turn, char = list(gamePlayVars.keys())[0], gamePlayVars[list(gamePlayVars.keys())[0]]
    while True:
        print(f"Hello {turn}, which position would you like to move on? ", end = '\n')
        if check_avail_chars(avail_chars, char):
            while True:
                while True:
                    print("Position can be either 'top-L', 'top-M', 'top-R', 'mid-L', 'mid-M', 'mid-R', 'low-L', 'low-M', 'low-R'")
                    position = input()
                    if position in theBoard.keys():
                        break
                    else:
                        print("That is not a position on the board")
                if theBoard[position] == ' ':
                    break
                else:
                     if theBoard[position] in avail_chars.keys():
                        print("Board position is already occupied. See the board and see which positons are empty.")
                        print()
                        printBoard(theBoard)
            theBoard[position] = char
            avail_chars[char] = avail_chars.setdefault(char, 0) - 1
            print()
            print(printBoard(theBoard))
        else:
            print("You have zero characters available. Define where you would like to move from and to")
            printBoard(theBoard)
            while True:
                print(f"{turn}, where would you like to move from? Make sure you are moving from a position that has your character. ")
                source = input()
                if theBoard[source] != char:
                    print("That position does not contain your character. Take a good look at the Board.")
                    printBoard(theBoard)
                    print("Position can be either 'top-L', 'top-M', 'top-R', 'mid-L', 'mid-M', 'mid-R', 'low-L', 'low-M', 'low-R'")
                else:
                    print()
                    break
            while True:
                print(f"{turn}, where would you like to move to? Make sure you are moving to an empty positon. ")
                destination = input()
                if theBoard[destination] != ' ':
                    print("That position is not empty. Take a good look at the Board.")
                    printBoard(theBoard)
                    print("Position can be either 'top-L', 'top-M', 'top-R', 'mid-L', 'mid-M', 'mid-R', 'low-L', 'low-M', 'low-R'")
                else:
                    print()
                    break
            theBoard[source] = ' '
            theBoard[destination] = char
            print(printBoard(theBoard))
        if gameCheck(theBoard, char):
            print(f"Congratulations {turn}, you just got a straight arrangement. Game over!!!")
            printBoard(theBoard)
            print('* ' * 20)
            break
        else:
            if turn == list(gamePlayVars.keys())[0] and char == gamePlayVars[list(gamePlayVars.keys())[0]]:
                turn, char = list(gamePlayVars.keys())[1], gamePlayVars[list(gamePlayVars.keys())[1]]
            else:
                turn, char = list(gamePlayVars.keys())[0], gamePlayVars[list(gamePlayVars.keys())[0]]
    return gamePlayVars

def resetgameVar():
    gameVar = shelve.open(os.path.join(os.path.abspath('.'), 'shelfvar', 'ticTacVars')) #a shelf file with game variables stored
    theBoard = gameVar['theBoard'] #the game board variable is retrieved from the shelf file
    avail_chars = gameVar['avail_chars'] #the game characters are retrieved from the shelf file
    gameVar.close()
    return (theBoard, avail_chars)

def playIter():
    gameVar = shelve.open(os.path.join(os.path.abspath('.'), 'shelfvar', 'ticTacVars')) #a shelf file with game variables stored
    theBoard = gameVar['theBoard'] #the game board variable is retrieved from the shelf file
    avail_chars = gameVar['avail_chars'] #the game characters are retrieved from the shelf file
    gamePlayVars = getUsersVar(avail_chars)
    playerVars = gamePlay(theBoard, avail_chars, gamePlayVars)   
    while True:
        print("Would you like to play again? Reply with 'Y' to replay and 'N' to exit")
        while True:
            reply = str.upper(input())
            if reply == 'Y' or reply == 'N':
                break
            else:
                print("Check your input. Reply is 'Y' or 'N'(case insensitive)")
        if reply == 'Y':
            print('Reloading game with existing variables.')
            print('* ' * 20, end = '\n')
            print('__' * 20)
            gamePlay(resetgameVar()[0], resetgameVar()[1], playerVars)
        elif reply == 'N':
            gameVar.close()
            break