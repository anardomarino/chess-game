default_board_state = 	[['br','bn','bb','bq','bk','bb','bn','br'],
						 ['bp','bp','bp','bp','bp','bp','bp','bp'],
						 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 ['ee','ee','ee','ee','ee','ee','ee','ee'],
						 ['wp','wp','wp','wp','wp','wp','wp','wp'],
						 ['wr','wn','wb','wq','wk','wb','wn','wr']]

class Board:
	def __init__(self, perspective):
		"""
		Initializes Board Instance
		Takes into account the perspective of play (Black or White
			at the bottem)
		"""
		if perspective == 'BLACK':
			self.state = default_board_state[::-1]
		else:
			self.state = default_board_state

	def __repr__(self):
		"""
		For Debugging, string format of board state
		"""
		toprint = ""
		for i in self.state:
			toprint += str(i) + "\n"
		return toprint

	def __len__(self):
		return len(self.state)

	def getState(self):
		return self.state

	def getPieceName(self, abbr):
		"""
		Translates abbreviation encoding into piece
			name for display
		"""
		name = ""
		if 'b' == abbr[0]:
			name += "Black "
		else:
			name += "White "

		if 'r' == abbr[1]:
			name += "Rook"
		if 'n' == abbr[1]:
			name += "Knight"
		if 'b' == abbr[1]:
			name += "Bishop"
		if 'q' == abbr[1]:
			name += "Queen"
		if 'k' == abbr[1]:
			name += "King"
		if 'p' == abbr[1]:
			name += "Pawn"
		return name

	def movePiece(self, movement_info):
		"""
		Actuates instructions from movement_info
		movement_info - tuple of tuples
			((oldRow,oldCol),(newRow,newCol))
		Handles piece movements and captures
		"""
		narrate = "" # Message to return
		capture = False
		old_r = movement_info[0][0]
		old_c = movement_info[0][1]
		new_r = movement_info[1][0]
		new_c = movement_info[1][1]

		from_piece = self.state[old_r][old_c]
		to___piece = self.state[new_r][new_c]

		# Move
		self.state[new_r][new_c] = self.state[old_r][old_c]
		self.state[old_r][old_c] = "ee"

		if self.state[new_r][new_c][1] == 'p' and (new_r == 0 or new_r == 7):
			self.state[new_r][new_c] = self.state[new_r][new_c][0] + 'q'

		return narrate

if __name__ == "__main__":
	uut = Board("WHITE")
	print(uut)
	uut = Board("BLACK")
	print(uut)