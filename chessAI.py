from chessLogistics import *
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from piece_vals import *

values = {'e' : 0,
		  'p' : 1,
		  'n' : 3,
		  'b' : 3,
		  'r' : 5,
		  'q' : 9,
		  'k' : 9}

class ChessAI:
	def __init__(self, name, color, behavior = 'random'):
		self.name = name
		self.color = color
		# Get opponent color for quick reference
		if color == 'WHITE':
			self.opcol = 'BLACK'
		else:
			self.opcol = 'WHITE'
		self.type = "AI"
		self.behavior = behavior
		self.rules = Rules()

	def getName(self):
		return self.name 

	def getColor(self):
		return self.color 

	def getType(self):
		return self.type

	def getMove(self, board, orientation):
		if self.behavior == 'random':
			return self.getRandomMove(board, orientation)
		elif self.behavior == 'aggro':
			return self.getAggroMove(board, orientation)
		elif self.behavior == 'value':
			return self.getValueMove(board, orientation)
		elif self.behavior == 'minimax1':
			return self.minimaxmove(board, orientation)
		elif self.behavior == 'alphabeta':
			return self.alphaBetaPruneMove(board, orientation)

		return self.getRandomMove(board, orientation)

	def getRandomMove(self, board, orientation):
		"""
		returns random move from possible moves
		"""
		if self.color == "BLACK":
			my_color = 'b'
		else:
			my_color = 'w'

		my_pieces = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == my_color:
					if self.rules.getValidMoves(board, self.color, (r,c), orientation):
						my_pieces.append((r,c))
		from_coord = my_pieces[random.randint(0,len(my_pieces)-1)]
		piece_moves = self.rules.getValidMoves(board, self.color, from_coord, orientation)
		to_coord = piece_moves[random.randint(0,len(piece_moves)-1)]

		return (from_coord, to_coord)

	def getAggroMove(self, board, orientation):
		"""
		returns random capture move from possible moves
		otherwise performs random move
		"""
		if self.color == "BLACK":
			my_color = 'b'
			enemy_color = 'w'
		else:
			my_color = 'w'
			enemy_color = 'b'

		my_pieces = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == my_color:
					if self.rules.getValidMoves(board, self.color, (r,c), orientation):
						my_pieces.append((r,c))
		from_coord = my_pieces[random.randint(0,len(my_pieces)-1)]
		piece_moves = self.rules.getValidMoves(board, self.color, from_coord, orientation)
		to_coord = piece_moves[random.randint(0,len(piece_moves)-1)]

		aggro_moves = []
		for piece in my_pieces:
			for move in self.rules.getValidMoves(board, self.color, piece, orientation):
				if board[move[0]][move[1]][0] == enemy_color:
					aggro_moves.append((piece, move))
		if len(aggro_moves) > 0:
			chosen = aggro_moves[random.randint(0,len(aggro_moves)-1)]
			from_coord = chosen[0]
			to_coord = chosen[1]

		return (from_coord, to_coord)

	def getValueMove(self, board, orientation):
		"""
		performs the most valuable capture from possible moves according to 
			values dictionary
		otherwise performs random move
		"""
		if self.color == "BLACK":
			my_color = 'b'
			enemy_color = 'w'
		else:
			my_color = 'w'
			enemy_color = 'b'

		my_pieces = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == my_color:
					if self.rules.getValidMoves(board, self.color, (r,c), orientation):
						my_pieces.append((r,c))
		from_coord = my_pieces[random.randint(0,len(my_pieces)-1)]
		piece_moves = self.rules.getValidMoves(board, self.color, from_coord, orientation)
		to_coord = piece_moves[random.randint(0,len(piece_moves)-1)]

		aggro_moves = []
		for piece in my_pieces:
			for move in self.rules.getValidMoves(board, self.color, piece, orientation):
				if board[move[0]][move[1]][0] == enemy_color:
					value = values[board[move[0]][move[1]][1]]
					aggro_moves.append((piece, move, value))
		if len(aggro_moves) > 0:
			aggro_moves = sorted(aggro_moves, key = lambda x : x[2], reverse = True)
			chosen = aggro_moves[0]
			from_coord = chosen[0]
			to_coord = chosen[1]

		return (from_coord, to_coord)

	def getMinimax1Move(self, board, orientation):
		"""
		maximizes value gained in captures and losses from set of moves
			up to 1 layer of recursion
		"""
		if self.color == 'BLACK':
			my_color = 'b'
			enemy_color = 'w'
		else:
			my_color = 'w'
			enemy_color = 'b'

		moves = []
		scores = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == my_color:
					for i in self.rules.getValidMoves(board, self.color, (r,c), orientation):
						moves.append(((r,c), i))
						scores.append(values[board[i[0]][i[1]][1]])
		for j in range(len(moves)):
			almost_board = deepcopy(board)
			piece = almost_board[moves[j][0][0]][moves[j][0][1]]
			almost_board[moves[j][0][0]][moves[j][0][1]] = 'ee'
			almost_board[moves[j][1][0]][moves[j][1][1]] = piece 
			scores[j] -= (self.getEnemyPotentialScore(almost_board, orientation))
		max_score = max(scores)
		max_moves = []
		for i in range(len(scores)):
			if scores[i] == max_score:
				max_moves.append(moves[i])
		return max_moves[random.randint(0,len(max_moves)-1)]

	def getEnemyPotentialScore(self, board, orientation):
		"""
		analyzes enemy moves from a given board and gives it a rating
		based on presence of friendly pieces after all possible moves
		of the enemy
		"""
		if self.color == 'BLACK':
			my_color = 'b'
			enemy_color = 'w'
			ecolor = "WHITE"
		else:
			my_color = 'w'
			enemy_color = 'b'
			ecolor = "BLACK"

		scores = []
		moves = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == enemy_color:
					for i in self.rules.getValidMoves(board, ecolor, (r,c), orientation):
						moves.append(((r,c), i))
		for move in moves:
			temp_board = deepcopy(board)
			piece = temp_board[move[0][0]][move[0][1]]
			temp_board[move[0][0]][move[0][1]] = 'ee'
			temp_board[move[1][0]][move[1][1]] = piece 

			# Rate board
			temp_score = 0
			for r in range(len(board)):
				for c in range(len(board)):
					if temp_board[r][c][0] == my_color:
						temp_score += values[temp_board[r][c][1]]
			scores.append(temp_score)

		return sum(scores)

	def getMyPieces(self, board, side):
		pieces = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == side[0].lower():
					pieces.append((r,c))
		return pieces

	def getPieceMoves(self, board, side, pieces, orientation):
		moves = []
		for piece in pieces:
			piece_moves = self.rules.getValidMoves(board, side, piece, orientation)
			for i in piece_moves:
				moves.append((piece,i))
		return moves

	def potBoards(self, board, side, pieces, orientation):
		boards = []
		scores = []
		done = True
		for piece in pieces:
			piece_moves = self.rules.getValidMoves(board, side, piece, orientation)
			for i in piece_moves:
				done = False
				if board[i[0]][i[1]][1] == 'k':
					print('k')
					continue
				boards.append(self.getNewBoard(board, (piece,i)))
				scores.append(self.scoreBoard(boards[-1], side, orientation))
		if done:
			return []
		base = list(zip(boards, scores))
		base = sorted(base, key = lambda x : x[1], reverse = False)
		try:
			boards = (list(zip(*base))[0])
			return boards
		except:
			return boards

	# def scoreBoard(self, board, side):
	# 	score = 0
	# 	for r in range(len(board)):
	# 		for c in range(len(board)):
	# 			piece = board[r][c]
	# 			if piece == 'ee':
	# 				continue
	# 			else:
	# 				mine = (piece[0]==side[0].lower())
	# 				score += (mine - (not mine))*(values[piece[1]])
	# 	return score

	def scoreBoard(self, board, side, orientation):
		score = 0
		for r in range(len(board)):
			for c in range(len(board)):
				ally, name = board[r][c][0], board[r][c][1]
				if name != 'e':
					score += dynamicValue(ally, name, side, (r,c), orientation)
		return score

	def getNewBoard(self, board, move):
		"""
		generates new board instance from move
		move - tuple of tuples
			((fr,fc),(tr,tc))
		"""
		fr,fc = move[0]
		tr,tc = move[1]
		temp_board = deepcopy(board)
		piece = temp_board[fr][fc]
		temp_board[fr][fc] = 'ee'

		# Check if pawn gets queened
		if piece[1] == 'p' and (tr == 7 or tr == 0):
			temp_board[tr][tc] = piece[0] + 'q'
		else:
			temp_board[tr][tc] = piece 

		return temp_board

	def stepDownBoard(self, board, my_side, enemy_side, orientation, layers = 0, this_layer = 0):
		if this_layer%2 == 0:
			pieces = self.getMyPieces(board,my_side)
			moves = self.getPieceMoves(board,my_side,pieces,orientation)
		else:
			pieces = self.getMyPieces(board,enemy_side)
			moves = self.getPieceMoves(board,enemy_side,pieces,orientation)

		if len(moves) == 0:
			if this_layer%2 == 0:
				return self.scoreBoard(board, my_side)
			else:
				return self.scoreBoard(board, enemy_side)

		boards = []
		scores = []

		for move in moves:
			boards.append(self.getNewBoard(board, move))
			scores.append(self.scoreBoard(boards[-1], my_side))
		if layers == 0:
			return moves[np.argmax(scores)]
		elif this_layer == 0:
			steps = []
			for board in boards:
				steps.append(self.stepDownBoard(board, my_side, enemy_side, orientation, layers, this_layer + 1))
			return moves[np.argmax(steps)]
		elif layers == this_layer:
			self.opcount += 1
			if this_layer%2 == 0:
				return max(scores)
			else:
				return min(scores)
		else:
			steps = []
			for i in range(len(boards)):
				steps.append(self.stepDownBoard(boards[i], my_side, enemy_side, orientation, layers, this_layer + 1))
			if this_layer%2 == 0:
				return max(steps)
			else:
				return min(steps)

	def minimaxmove(self, board, orientation):
		if self.color == 'WHITE':
			enemy_side = 'BLACK'
		else:
			enemy_side = 'WHITE'
		self.opcount = 0
		move = self.stepDownBoard(board, self.color, enemy_side, orientation, layers = 4)
		print('opcount =', self.opcount)
		return move

	def alphaBeta(self, board, orientation, this_player = True, depth = 0, a = float('-inf'), b = float('inf')):
		if depth == 0:
			self.count += 1
			return self.scoreBoard(board, self.color, orientation)
		side   = this_player*self.color + (not this_player)*self.opcol
		pieces = self.getMyPieces(board, side)
		boards = self.potBoards(board, side, pieces, orientation)
		if len(boards) == 0:
			self.count += 1
			return self.scoreBoard(board, self.color, orientation)

		# moves  = self.getPieceMoves(board, side, pieces, orientation)
		# # If no possible moves / deadend, return board value
		# if len(moves) == 0:
		# 	self.count += 1
		# 	return self.scoreBoard(board, self.color)
		# boards = []
		# for move in moves:
		# 	boards.append(self.getNewBoard(board, move))

		if this_player:
			value = float('-inf')
			for tboard in boards:
				value = max(value, self.alphaBeta(tboard, orientation, False, depth - 1, a, b))
				a     = max(value, a)
				if a >= b:
					break 	# b cutoff
			return value
		else:
			value = float('inf')
			for tboard in boards:
				value = min(value, self.alphaBeta(tboard, orientation,  True, depth - 1, a, b))
				b     = min(value, b)
				if a >= b:
					break 	# a cutoff
			return value

	def alphaBetaPruneMove(self, board, orientation, depth = 2):
		# Problem with eliminating branches
		# Does not take into consideration some of my moves are
		#	more likely than others, therefore moves to the position
		#	that would be best for if I was oblivious to an opening
		# I.e. too aggressive?
		pieces = self.getMyPieces(board, self.color)
		moves  = self.getPieceMoves(board, self.color, pieces, orientation)
		boards = []
		scores = []
		self.count = 0
		for move in moves:
			boards.append(self.getNewBoard(board, move))
		for tboard in boards:
			scores.append(self.alphaBeta(tboard, orientation, True, depth, -10000, 10000))
		print('node count =', self.count)
		print(moves)
		print(scores)
		print(len(moves))
		return moves[np.argmax(scores)]

if __name__ == '__main__':
	default_board_state = 	[['br','bn','bb','bq','bk','bb','bn','br'],
						 	 ['bp','bp','bp','bp','bp','bp','bp','bp'],
						 	 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 	 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 	 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 	 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 	 ['wp','wp','wp','wp','wp','wp','wp','wp'],
						 	 ['wr','wn','wb','wq','wk','wb','wn','wr']]

	# counts = []
	# times  = []
	# ai = ChessAI('a','BLACK')
	# for i in range(4):
	# 	start = time.time()
	# 	print(ai.alphaBetaPruneMove(default_board_state, 1, i))
	# 	end = time.time()
	# 	counts.append(ai.count)
	# 	times.append(end-start)
	# 	print(end-start)
	# plt.plot(counts, times)
	# plt.show()

	ai = ChessAI('a','BLACK')
	start = time.time()
	print(ai.alphaBetaPruneMove(default_board_state, 1, 2))
	end = time.time()
	print(end-start)