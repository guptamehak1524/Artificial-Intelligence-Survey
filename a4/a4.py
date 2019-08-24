# a4.py
# MEHAK GUPTA
# 301311972
# ASSIGNMENT 4

#Tic Tac Toe with Pure Monte Carlo Tree Search

import random
import copy

available_spots = ['', '2', '3', '4', '5', '6', '7', '8', '9']
state = ['-1', '1', '2', '3', '4', '5', '6', '7', '8', '9']


#  basic structure of the play
def drawBoard(board):
    print('    |    |')
    print(' ' + board[1] + '  | ' + board[2] + '  | ' + board[3])
    print('    |    |')
    print('--------------')
    print('    |    |')
    print(' ' + board[4] + '  | ' + board[5] + '  | ' + board[6])
    print('    |    |')
    print('--------------')
    print('    |    |')
    print(' ' + board[7] + '  | ' + board[8] + '  | ' + board[9])
    print('    |    |')


 # decides who starts .. if 0 then human else computer
def first_turn():
    x = random.randint(0,1)
    return x


# human turn - human decides a move from the available slots
def human():
    global available_spots
    global state
    move = ''
    move = input("HUMANS'S TURN : Pick a spot -- ")
    while move not in available_spots:
        print("Invalid Move")
        move = input("HUMANS'S TURN : Pick a spot -- ")
    state[int(move)] = 'O'
    available_spots.remove(move)


# checks after every move if the last player who made a move is a winner 
# or not
def isWinner(board, player):
    return ((board[7] == player and board[8] == player and board[9] == player) or # across the top
          (board[4] == player and board[5] == player and board[6] == player) or # across the middle
          (board[1] == player and board[2] == player and board[3] == player) or # across the bottom
          (board[7] == player and board[4] == player and board[1] == player) or # down the left side
          (board[8] == player and board[5] == player and board[2] == player) or # down the middle
          (board[9] == player and board[6] == player and board[3] == player) or # down the right side
          (board[7] == player and board[5] == player and board[3] == player) or # diagonal
          (board[9] == player and board[5] == player and board[1] == player)) # diagonal
         

# Computer's Turn - it takes k number of iterations and play k random playouts
# with every possible move and calculates the score for every move and returns
# the move with the largest score
def computer(iterations = 200):
    global available_spots
    max_count = -100000
    move = ''
    for i in available_spots:
        count  = 0
        for j in range(iterations):
            play_result = random_playout(i)
            count += play_result  
        if count > max_count:
            max_count = count
            move = i
    # takes the final move and make a new state
    state[int(move)] = 'X'
    available_spots.remove(move)
    print("COMPUTER'S TURN")


# this function makes copies of both state and available moves and plays random 
# games with self in order to find the best move
def random_playout(move): 
  random_state = copy.deepcopy(state)
  random_available_spots = copy.deepcopy(available_spots)
  random_state[int(move)] = 'X'
  random_available_spots.remove(move)
  if(isWinner(random_state, 'X')):
      return 2

  while available_spots:
      if(len(random_available_spots) == 0):
          return 1
      computer1_move = random.choice(random_available_spots)
      random_state[int(computer1_move)] = 'O'
      random_available_spots.remove(computer1_move)
      if(isWinner(random_state, 'O')):
          return -2
      if(len(random_available_spots) == 0):
          return 1
      computer2_move = random.choice(random_available_spots)
      random_state[int(computer2_move)] = 'X'
      random_available_spots.remove(computer2_move)
      if(isWinner(random_state, 'X')):
          return 2
  return 1


# starts a new game
def play_a_new_game():
    global state
    global available_spots
    print()
    print("|*************************************************|")
    print("|            WELCOME TO TIC-TAC-TOE               |")
    print("|            HUMAN (O)   COMPUTER (X)             |")
    print("|                                                 |")
    print("| The game will randmly choose one of the players |")
    print("| to go first in the game.                        |")
    print("|                                                 |")
    print("| RULES - Every player has to choose one spot     |")
    print("| out of the available spots/numbers when it is . |")
    print("| there turn.                                     |")
    print("|                                                 |")
    print("|*************************************************|")
    print()
    drawBoard(state)
    if first_turn()==0:
        human()
        flag = 1
    else:
        computer()
        flag  = 0
    drawBoard(state)
    while available_spots:
        if flag == 0:
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break
            human()
            drawBoard(state)
            if(isWinner(state, 'O')):
                print("********")
                print("Winner IS HUMAN")
                print("********")
                break
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break
            computer()
            drawBoard(state)
            if(isWinner(state, 'X')):
                print("********")
                print("Winner IS COMPUTER")
                print("********")
                break
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break
        else:
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break

            computer()
            drawBoard(state)
            if(isWinner(state, 'X')):
                print("********")
                print("Winner IS COMPUTER")
                print("********")
                break
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break
            human()
            drawBoard(state)
            if(isWinner(state, 'O')):
                print("********")
                print("Winner IS HUMAN")
                print("********")
                break
            if(len(available_spots) == 0):
                print("********")
                print("DRAW")
                print("********")
                break


#  main function
if __name__ == '__main__':
     play_a_new_game()


