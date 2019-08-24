# ASSIGNMENT 1
# MEHAK GUPTA
# 301311972

# a1.py
import random
import time
from search import *

#QUESTION 1 
eight_puzzle_temp = EightPuzzle((1,2,3,4,5,6,7,8,0))
def make_rand_8puzzle():
	x = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	new_state = random.sample(x, len(x))
	while new_state:
		if eight_puzzle_temp.check_solvability(tuple(new_state)):
			return EightPuzzle(tuple(new_state))
		new_state = random.sample(x, len(x))


def display(state):
	count =0
	for val in state:
		if not count % 3:
			print()
		if(val == 0):
			val = '*'
		print (val, end=' ')
		count += 1
	print()

#_____________________________________________________________

#QUESTION 2

def eightPuzzle_manhattan(node):
		matrix = convert_to_matrix(node.state)
		mhd = 0
		for i in range(3):
			for j in range(3):
				if matrix[i][j] != 0:
					x, y = divmod(matrix[i][j]-1, 3)
					mhd += abs(x - i) + abs(y - j)
		return mhd

# Calculates Maximum of misplaced tiles heuristic and manhattan distance heuristic
def eightPuzzle_maximum(node):
	x = eightPuzzle_manhattan(node)
	y = eight_puzzle_temp.h(node)
	return max(x,y)

#Helper functions
def convert_to_matrix(state):
	y = []
	x = []
	for i,item in enumerate(state):
		x.append(item)
		if (i+1)%3 == 0:
			y.append(x)
			x =[]
	return y
# ______________________________________________________________________________

#QUESTION 3

class YPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a Y-board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 1:
            possible_actions.remove('LEFT')
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        if index_blank_square == 2 :
            possible_actions.remove('LEFT')
        if index_blank_square == 3:
            possible_actions.remove('UP')
        if index_blank_square == 4:
            possible_actions.remove('RIGHT')
        if index_blank_square == 5:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
        if index_blank_square == 8:
            possible_actions.remove('LEFT')
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        # NOTE - results given only for the VALID ACTIONS

        # blank is the index of the blank square
        index_blank_square = self.find_blank_square(state)
        new_state = list(state)

        if index_blank_square == 0:
            delta = {'DOWN':2}
        if index_blank_square == 1:
            delta = {'DOWN':3}
        if index_blank_square == 2 :
        	delta = {'UP':-2, 'DOWN':3, 'RIGHT':1}
        if index_blank_square == 3:
            delta = {'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        if index_blank_square == 4:
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1}
        if index_blank_square == 5:
            delta = {'UP':-3, 'RIGHT':1}
        if index_blank_square == 6:
            delta = {'UP':-3, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
        if index_blank_square == 7:
            delta = {'UP':-3, 'LEFT':-1}
        if index_blank_square == 8:
            delta = {'UP':-2}
      
        neighbor = index_blank_square + delta[action]
        new_state[index_blank_square], new_state[neighbor] = new_state[neighbor], new_state[index_blank_square]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

#-----------------------------------

# Copied from search.py and did some modifications to print the length of 
# the solution and number of nodes removed from frontier

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    count_pop = 0
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        count_pop = count_pop + 1
        if problem.goal_test(node.state):
            print("Length of the solution = {}".format(len(node.path())))
            print("Number of nodes that were removed from frontier = {}".format(count_pop))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print("NOT SOLVABLE")
    return None


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def ypuzzle_manhattan(node):
        state = node.state
        mhd = 0
        index_goal = {0:[3,1], 1:[0,0], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
        index = {0:[0,0], 1:[0,2], 2:[1,0], 3:[1,1], 4:[1,2], 5:[2,0], 6:[2,1], 7:[2,2], 8:[3,1]}
        
        for i in range(len(state)):
            x1, y1 = index[i]
            x2, y2 = index_goal[state[i]]
            mhd += abs(x1 - x2) + abs(y1 - y2) 
        
        return mhd

# Calculates Maximum of misplaced tiles heuristic and manhattan distance heuristic
def ypuzzle_maximum(node):
	x = ypuzzle_manhattan(node)
	y = ypuzzle.h(node)
	return max(x, y)

#_____________________________________________________________


# TESTS FOR GIVEN FUNCTIONS

#---------PART 1---------------------------
new_state = make_rand_8puzzle()
display(new_state.initial)

#--------PART 2----------------------------
for i in range(10):
	
	eight_puzzle = make_rand_8puzzle()
	print("PUZZLE = {}". format(eight_puzzle.initial))

	print("EIGHT PUZZLE - MISPLACED TILE HEURISTIC")
	start_time = time.time()
	astar_search(eight_puzzle, eight_puzzle.h)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()

	print("EIGHT PUZZLE - MANHATTAN DISTANCE HEURISTIC")
	start_time = time.time()
	astar_search(eight_puzzle, eightPuzzle_manhattan)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()

	print("EIGHT PUZZLE - MAXIUM OF BOTH")
	start_time = time.time()
	astar_search(eight_puzzle, eightPuzzle_maximum)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()

# -------------PART 3----------------------
ypuzzle_list = [
list((1,2,8,6,4,3,7,5,0)), 
list((0,2,1,3,8,5,4,6,7)), 
list((1,2,0,5,8,4,3,6,7)),
list((1,0,8,6,2,3,5,4,7)),
list((1,0,4,5,2,3,6,8,7)),
list((1,2,8,0,6,3,5,4,7)),
list((0,2,1,6,4,8,3,5,7)),
list((1,2,3,8,6,5,7,4,0)),
list((1,2,5,3,8,4,7,6,0)),
list((1,2,3,8,6,5,4,0,7))]

for i in range(10):
	ypuzzle_tuple = tuple(ypuzzle_list[i])
	ypuzzle = YPuzzle(ypuzzle_tuple)

	print("PUZZLE = {}". format(ypuzzle.initial))
	print("YPUZZLE - MISPLACED TILE HEURISTIC")
	start_time = time.time()
	astar_search(ypuzzle, ypuzzle.h)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()

	print("YPUZZLE - MANHATTAN DISTANCE HEURISTIC")
	start_time = time.time()
	astar_search(ypuzzle, ypuzzle_manhattan)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()

	print("YPUZZLE - MAXIUM OF BOTH")
	start_time = time.time()
	astar_search(ypuzzle, ypuzzle_maximum)
	elapsed_time = time.time() 
	print(elapsed_time - start_time)
	print("----------------------")
	print()




