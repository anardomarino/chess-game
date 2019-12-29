from copy import deepcopy

class Rules:
	def isCheckmate(self, board, color, orientedWhite):
		my_color = color[0].lower()
		validMoves = []
		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == my_color:
					validMoves += self.getValidMoves(board, color, (r,c), orientedWhite)
		if len(validMoves) > 0:
			return False,False
		elif self.isInCheck(board, color, orientedWhite):
			return True, False
		return True, True

	def getValidMoves(self, board, side, from_coord, orientedWhite):
		valid = []
		for r in range(len(board)):
			for c in range(len(board)):
				to_coord = r,c 
				if self.isLegalMove(board, side, from_coord, to_coord, orientedWhite):
					if not self.doesCheck(board, side, from_coord, to_coord, orientedWhite):
						valid.append(to_coord)
		return valid

	def isLegalMove(self, board, side, from_coord, to_coord, orientedWhite):
		"""
		Determines if a given move is legal
		board - Board instance
		side  - "WHITE" or "BLACK" dependant on player's side
		from_coord - tuple of len 2, (x,y). Start pos
		to_coord - tuple of len 2, (x,y). End pos
		orientation - 1 if white on the bottom, 0 if else
		"""

		if from_coord == to_coord:
			return False

		fr,fc = from_coord
		tr,tc = to_coord
		if tr >= len(board) or tc >= len(board) or tr < 0 or tc < 0:
			return False

		f_piece = board[fr][fc]
		t_piece = board[tr][tc]

		# logic assignments
		if side == 'WHITE':
			enemy_color = 'b'
			isWhite = 1
		else:
			enemy_color = 'w'
			isWhite = 0

		if 'p' == f_piece[1]:
			# Pawn
			#
			#
			movement = 1
			startRow = 1
			if (side == "WHITE" and orientedWhite) or (side == "BLACK" and not orientedWhite):
				movement = -1
				startRow = 6
			if tr == (fr + movement) and tc == fc and t_piece == 'ee':
				# forward movement
				return True
			if fr == startRow and tr == (fr + 2*movement) and tc == fc and t_piece == 'ee':
				# first movement 2 spaces
				if self.isClearPath(board, from_coord, to_coord):
					return True
			if tr == (fr + movement) and abs(tc - fc) == 1 and t_piece[0] == enemy_color:
				# capturing enemy piece
				return True

		elif 'r' == f_piece[1]:
			# Rook
			#
			# Exclusive Vertical movement and Horizontal movement
			# Row stays constant or column stays constant
			if (tr == fr or tc == fc) and (t_piece == 'ee' or t_piece[0] == enemy_color):
				if self.isClearPath(board, from_coord, to_coord):
					return True

		elif 'b' == f_piece[1]:
			# Bishop
			#
			# Row change magnitude equal to col change magnitude
			# = Diagonal movement
			if (abs(tr - fr) == abs(tc - fc)) and (t_piece == 'ee' or t_piece[0] == enemy_color):
				if self.isClearPath(board, from_coord, to_coord):
					return True

		elif 'n' == f_piece[1]:
			# Knight
			#
			# 2 squares in one axis, 1 in the other
			# = L movement
			r_dist = abs(tr-fr)
			c_dist = abs(tc-fc)
			if ((r_dist == 2 and c_dist == 1) or (r_dist == 1 and c_dist == 2)) and (t_piece == 'ee' or t_piece[0] == enemy_color):
				return True

		elif 'q' == f_piece[1]:
			# Queen
			#
			# Rook and Bishop movement
			if (tr == fr or tc == fc) and (t_piece == 'ee' or t_piece[0] == enemy_color):
				if self.isClearPath(board, from_coord, to_coord):
					return True
			if (abs(tr - fr) == abs(tc - fc)) and (t_piece == 'ee' or t_piece[0] == enemy_color):
				if self.isClearPath(board, from_coord, to_coord):
					return True

		elif 'k' == f_piece[1]:
			# King
			#
			# magnitude of 1 square
			r_dist = abs(tr-fr)
			c_dist = abs(tc-fc)
			if t_piece == 'ee' or t_piece[0] == enemy_color:
				if r_dist == 0 and c_dist == 1:
					return True
				elif r_dist == 1 and c_dist == 0:
					return True
				elif r_dist == 1 and c_dist == 1:
					return True

		# No cases match, invalid move
		return False


	def doesCheck(self, board, side, from_coord, to_coord, orientedWhite):
		fr,fc = from_coord
		tr,tc = to_coord
		from_piece = board[fr][fc]

		test_board = deepcopy(board)
		test_board[tr][tc] = from_piece
		test_board[fr][fc] = 'ee'

		return self.isInCheck(test_board, side, orientedWhite)

	def isInCheck(self, board, side, orientedWhite):
		if side == "WHITE":
			enemy_color = 'b'
			enemy_side = "BLACK"
			my_color = 'w'
		else:
			enemy_color = 'w'
			enemy_side = "WHITE"
			my_color = 'b'

		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c] == my_color + 'k':
					king_pos = (r,c)

		for r in range(len(board)):
			for c in range(len(board)):
				if board[r][c][0] == enemy_color:
					try:
						# Test if there is a king_pos
						if self.isLegalMove(board, enemy_side, (r,c), king_pos, orientedWhite):
							return True
					except UnboundLocalError:
						return False
		return False

	def isClearPath(self, board, from_coord, to_coord):
		fr,fc = from_coord
		tr,tc = to_coord

		if abs(fr - tr) <= 1 and abs(fc - tc) <= 1:
			return True
		else:
			if fr == tr:
				new_from = (fr, fc + (fc < tc) - (fc > tc))
			elif fc == tc:
				new_from = (fr + (fr < tr) - (fr > tr), fc)
			else:
				new_from = (fr + (fr < tr) - (fr > tr), fc + (fc < tc) - (fc > tc))

		if board[new_from[0]][new_from[1]] != 'ee':
			return False
		return self.isClearPath(board, new_from, to_coord)