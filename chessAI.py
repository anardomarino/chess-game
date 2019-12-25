from chessLogistics import *
import random

values = {'p' : 1,
		  'n' : 3,
		  'b' : 3,
		  'r' : 5,
		  'q' : 9,
		  'k' : 4}

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

	def getRandomMove(self, board, orientation):
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