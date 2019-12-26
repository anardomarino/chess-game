from chessLogistics import *
import random
import numpy as np

values = {'e' : 0,
		  'p' : 1,
		  'n' : 3,
		  'b' : 3,
		  'r' : 5,
		  'q' : 9,
		  'k' : 20}

class ChessAI:
	def __init__(self, name, color, behavior = 'random'):
		self.name = name
		self.color = color
		self.type = "AI"
		self.behavior = behavior
		self.rules = Rules()

	def getMove(self):
		pass

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
			return self.getMinimax1Move(board, orientation)

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
			scores[j] += (self.getEnemyPotentialScore(almost_board, orientation))
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