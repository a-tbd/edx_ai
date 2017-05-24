""" Homework 1: 8 puzzle game
Three search algorithms (breadth first, depth first, and a star)
to find a path from a given board configuration to the 
winning configuration where the tiles 0 - 8 are in numerical order.


Useage: 
	>>> driver.py <search type> <board>
search type: bfs, dfs, ast
board: starting board config as a string of numbers, e.g. 0,1,2,3,4,5,6,7,8

Output:
	output.txt file with:
		path to goal, 
		cost of path, 
		nodes expanded,
		search depth,
		max search depth,
		running time,
		max ram useage
"""

#!/usr/bin/python

import collections
import heapq
import itertools
import resource
import sys
import timeit
import math
import pdb

class Board(object):
	actions = ((-1, 0), (1, 0), (0, -1), (0, 1))
	action_names = (('Up'), ('Down'), ('Left'), ('Right'))

	def __init__(self, board, parent = None, path = None, search_depth = 0, children = [], key = 0):
		self.board = board 
		self.parent = parent 
		self.path = path 
		self.search_depth = search_depth 
		self.children = children 
		self.key = key

	# reconfigures the board as a matrix
	def board_matrix(self):
		return [self.board[i:i+3] for i in range(0, len(self.board),3)]

	# gets the index of the empty space on the board
	def get_empty_space(self):
		matrix = self.board_matrix()
		for i in range(3):
			for j in range(3):
				if matrix[i][j] == 0:
					return i, j

	# generates list of moves that make up the start --> goal
	# recursion limit reached for some paths so non-recursive solution is included below
	def get_path(self):
	    #if self.parent.path:
	    # 	return self.parent.get_path() + [self.path]
	    #return [self.path]
	    path = []
	    currentNode = self
	    while currentNode.path != None:
	    	path.append(currentNode.path)
	    	currentNode = currentNode.parent
	    return path

	def __repr__(self):
		return str(self.board)

	def __eq__(self, other):
		return str(self.board) == str(other.board) 

	def __hash__(self):
		return hash(str(self.board))

class Frontier(object):
	def __init__(self, boards = collections.deque([]), board_set = set()):
		self.boards = boards 
		self.board_set = board_set 

	# adds to board.children valid child board configurations as objects
	def get_children(self, board):
		row, col = board.get_empty_space()
		valid_moves = []

		# checks all possible moves
		for i in range(len(board.actions)):
			row2 = row + board.actions[i][0]
			col2 = col + board.actions[i][1]

			# adds to list any valid move and path to get to the move
			if row2 >= 0 and row2 < 3 and col2 >= 0 and col2 < 3:
				matrix = list(board.board_matrix())

				aux = matrix[row2][col2]
				matrix[row2][col2] = 0
				matrix[row][col] = aux
				new_board = [matrix[r][c] for r in range(3) for c in range(3)]

				# create new board instance for valid move and add it to children
				child_board = Board(new_board, board, board.action_names[i], board.search_depth + 1)
				valid_moves.append(child_board)
		return valid_moves
	
	# adds a new board state to the frontier
	def add_node(self, node):
		self.boards.append(node)
		self.board_set.add(node)
		node.children = self.get_children(node)

	def __repr__(self):
		return str(self.boards)

# documentation on heap implementation: https://docs.python.org/2/library/heapq.html
class aStarFrontier(Frontier):
	def __init__(self, boards = [], board_set = set()):
		super(aStarFrontier, self).__init__()
		self.boards = [] 
		self.entry_finder = {}
		self.REMOVED = '<removed-task>'
		self.counter = itertools.count()

	def add_node(self, node):
		self.board_set.add(node)
		node.children = self.get_children(node)
		node.key = self.set_key(node)
		if node in self.entry_finder:
			remove_node(node)
		count = next(self.counter)
		entry = [node.key + node.search_depth, count, node]
		self.entry_finder[node] = entry

		heapq.heappush(self.boards, entry)

	def remove_node(self, node):
		entry = self.entry_finder.pop(node)
		entry[-1] = self.REMOVED

	def pop_node(self):
		while self.boards:
			key, count, node = heapq.heappop(self.boards)
			if not node is self.REMOVED:
				del self.entry_finder[node]
				return node
		raise KeyError('pop from an empty priority queue')

	def set_key(self, node):
		distances = { 0: (0, 0), 
					  1: (0, 1), 
					  2: (0, 2), 
					  3: (1, 0), 
					  4: (1, 1), 
					  5: (1, 2), 
					  6: (2, 0), 
					  7: (2, 1), 
					  8: (2, 2)  }
		total_distance = 0
		for i in range(len(node.board)):
			if node.board[i] != 0:
				current_loc = distances[i]
				goal_loc = distances[node.board[i]]
				total_distance += abs(goal_loc[0] - current_loc[0]) + abs(goal_loc[1] - current_loc[1])
		return total_distance


def bfs(board):
	frontier = Frontier()
	frontier.add_node(board)
	
	winning = Board([0,1,2,3,4,5,6,7,8])
	visited = set()

	# stats to track
	max_search_depth = 0
	nodes_expanded = 0

	while frontier.boards:
		state = frontier.boards.popleft()
		visited.add(state)

		max_search_depth = state.search_depth + 1

		if state == winning:
			return output(state, nodes_expanded, max_search_depth)
		else:
			nodes_expanded += 1
			for i in range(len(state.children)):
				if not state.children[i] in visited and not state.children[i] in frontier.board_set:
					frontier.add_node(state.children[i])
	print "no winner found"


def dfs(board):
	frontier = Frontier()
	frontier.add_node(board)
	
	winning = Board([0,1,2,3,4,5,6,7,8])
	visited = set()

	# stats to track
	max_search_depth = 0
	nodes_expanded = 0

	# while there are still boards to explore
	while frontier.boards:
		state = frontier.boards.pop()
		visited.add(state)

		if state.search_depth > max_search_depth:
			max_search_depth = state.search_depth

		if state == winning:
			return output(state, nodes_expanded, max_search_depth)
		else:
			nodes_expanded += 1
			for i in range(len(state.children) - 1, -1, -1):
				if not state.children[i] in visited and not state.children[i] in frontier.board_set:
					frontier.add_node(state.children[i])
	print "no winner found"


def ast(board):
	frontier = aStarFrontier()
	frontier.add_node(board)
	
	visited = set()

	# stats to track
	max_search_depth = 0
	nodes_expanded = 0

	while frontier.boards:
		state = frontier.pop_node()
		visited.add(state)

		if state.search_depth > max_search_depth:
			max_search_depth = state.search_depth

		if state.key == 0:
			return output(state, nodes_expanded, max_search_depth)
		else:
			nodes_expanded += 1
			for i in range(len(state.children)):
				if not state.children[i] in visited:
					if not state.children[i] in frontier.board_set:
						frontier.add_node(state.children[i])



def output(node, nodes_expanded, max_search_depth):
	max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss 
	running_time = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000) 
	path = node.get_path() 

	text = ['path_to_goal: ' + str(path),
			'cost_of_path: ' + str(len(path)),
			'nodes_expanded: ' + str(nodes_expanded),
			'search_depth: ' + str(node.search_depth),
			'max_search_depth: ' + str(max_search_depth),
			'running_time: ' + str(running_time),
			'max_ram_usage: '+ str(max_ram_usage)]

	with open('output.txt', 'w') as f:
	    f.write('\n'.join(text))

def main(argv):
	try:
		method, board = argv
	except:
		print 'useage: driver.py method board'
		sys.exit(2)
	
	board = Board([int(i) for i in board.split(',')])

	if method == 'bfs':
		bfs(board)
	elif method == 'dfs':
		dfs(board)
	elif method == 'ast':
		ast(board)
	else:
		print 'method must be bfs, dfs, or ast'
		sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])


