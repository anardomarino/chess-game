import tkinter as tk
from tkinter import messagebox
from player import *
from chessAI import *
from screens import *
from chess_ui import *
from chessLogistics import *

class Main:
	def __init__(self):
		self.app = Welcome()
		self.app.start()
		self.info = self.app.get_entry_info()

		self.rules = Rules()
		self.setup()
		if self.players[0].getType() == 'Player':
			color = 'WHITE'
		else:
			color = 'BLACK'
		self.board = Board(color)
		if color == 'WHITE': 
			self.orientation = 1
		else:
			self.orientation = 0
		self.gui = Game(self.orientation)
		self.close = False

	def setup(self):
		if self.info[0][1] == 'L':
			player1 = Player(self.info[0][0], 'WHITE')
		else:
			player1 = ChessAI(self.info[0][0], 'WHITE', behavior = 'value')
		if self.info[1][1] == 'L':
			player2 = Player(self.info[1][0], 'BLACK')
		else:
			player2 = ChessAI(self.info[1][0], 'BLACK', behavior = 'value')
		self.players = [player1, player2]

	def loop(self):
		current_player = 0 	# index of acting player
		turn_count = 0		# counter of turns taken
		while not self.rules.isCheckmate(self.board.getState(), self.players[current_player].getColor(), self.orientation)[0]:
			board = self.board.getState()
			current_color = self.players[current_player].getColor()
			if current_color == 'WHITE':
				turn_count += 1
			self.gui.draw(board)
			self.gui.printMessage(self.players[current_player].getName() + "\'s move.")

			if self.rules.isInCheck(board, current_color, self.orientation):
				self.gui.printMessage(self.players[current_player].getName() + " is in check.")

			if self.players[current_player].getType() == 'AI':
				movement = self.players[current_player].getMove(board, self.orientation)
			else:
				movement = self.gui.getPlayerInput(board, current_color)

			move = self.board.movePiece(movement)
			self.gui.printMessage(move)
			current_player = not current_player
		self.gui.printMessage("")
		if self.rules.isCheckmate(self.board.getState(), self.players[current_player].getColor(), self.orientation)[1]:
			self.gui.printMessage("Stalemate.")
		else:
			self.gui.printMessage("Checkmate.")
			winner_index = not current_player
			self.gui.printMessage(self.players[winner_index].getName() + " wins!")
		self.gui.draw(board)
		self.gui.printMessage("")
		while True:
			self.gui.getFinalInput()

if __name__ == "__main__":
	app = Main()
	app.setup()
	app.loop()