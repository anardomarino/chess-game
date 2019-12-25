import pygame
import os
from pygame.locals import *
from Board import *
from chessLogistics import *
from textBox import *

class Game:
	def __init__(self, orientation):
		os.environ['SDL_VIDEO_CENTERED'] = '1' # Center window
		self.orientation = orientation
		self.rules = Rules()
		self.loadImgs()
		self.screen = pygame.display.set_mode((850,500))
		pygame.init()
		pygame.display.init()
		pygame.display.set_caption("Chess")
		self.font = pygame.font.Font(None, 20)

		self.textBox = TextBox(self.screen, 525, 850, 50, 450)

		self.boardx_corner = 50
		self.boardy_corner = 50
	
	def loadImgs(self):
		self.squaresize = 50
		self.white 	= pygame.image.load("img/white.png")
		self.tan 	= pygame.image.load("img/tan.png")
		self.blue 	= pygame.image.load("img/blue.png")
		self.bp		= pygame.image.load("img/bp.png")
		self.br 	= pygame.image.load("img/br.png")
		self.bb 	= pygame.image.load("img/bb.png")
		self.bn 	= pygame.image.load("img/bn.png")
		self.bq 	= pygame.image.load("img/bq.png")
		self.bk 	= pygame.image.load("img/bk.png")
		self.wp		= pygame.image.load("img/wp.png")
		self.wr		= pygame.image.load("img/wr.png")
		self.wb		= pygame.image.load("img/wb.png")
		self.wn		= pygame.image.load("img/wn.png")
		self.wq		= pygame.image.load("img/wq.png")
		self.wk		= pygame.image.load("img/wk.png")

	def printMessage(self, message):
		self.textBox.add(message)

	def boardToScreen(self, coordinates):
		"""
		coordinates - tuple of r,c in terms of the board
		"""
		row,col = coordinates
		screenX = self.boardx_corner + col*self.squaresize
		screenY = self.boardy_corner + row*self.squaresize
		return screenX,screenY

	def screenToBoard(self, coordinates):
		"""
		coordinates - tuple of x,y in terms of the screen
		inverse of boardToScreen
		"""
		x,y = coordinates
		boardX = (x-self.boardx_corner)//self.squaresize
		boardY = (y-self.boardy_corner)//self.squaresize
		print('board', boardX, boardY)
		return boardY,boardX

	def draw(self, board, selSquares = []):
		self.textBox.draw()
		boardsize = len(board)

		# draw blank board
		even_odd = True
		for r in range(len(board)):
			for c in range(len(board)):
				x,y = self.boardToScreen((r,c))
				if even_odd:
					self.screen.blit(self.white, (x,y))
				else:
					self.screen.blit(self.tan, (x,y))
				even_odd = not even_odd
			even_odd = not even_odd

		# highlight selected squares
		for square in selSquares:
			x,y = self.boardToScreen(square)
			self.screen.blit(self.blue, (x,y))

		# draw pieces
		for r in range(len(board)):
			for c in range(len(board)):
				x,y = (self.boardToScreen((r,c))[0]-5, self.boardToScreen((r,c))[1]-5)
				if board[r][c] == 'bp':
					self.screen.blit(self.bp, (x,y))
				if board[r][c] == 'br':
					self.screen.blit(self.br, (x,y))
				if board[r][c] == 'bn':
					self.screen.blit(self.bn, (x,y))
				if board[r][c] == 'bb':
					self.screen.blit(self.bb, (x,y))
				if board[r][c] == 'bq':
					self.screen.blit(self.bq, (x,y))
				if board[r][c] == 'bk':
					self.screen.blit(self.bk, (x,y))
				if board[r][c] == 'wp':
					self.screen.blit(self.wp, (x,y))
				if board[r][c] == 'wr':
					self.screen.blit(self.wr, (x,y))
				if board[r][c] == 'wn':
					self.screen.blit(self.wn, (x,y))
				if board[r][c] == 'wb':
					self.screen.blit(self.wb, (x,y))
				if board[r][c] == 'wq':
					self.screen.blit(self.wq, (x,y))
				if board[r][c] == 'wk':
					self.screen.blit(self.wk, (x,y))

		pygame.display.flip()

	def getClickedSquare(self,mouseX,mouseY):
		#test function
		print("User clicked screen position x =",mouseX,"y =",mouseY)
		(row,col) = self.screenToBoard((mouseX,mouseY))
		if col < 8 and col >= 0 and row < 8 and row >= 0:
			print("  Chess board units row =",row,"col =",col)

	def getFinalInput(self):
		for e in pygame.event.get():
			if e.type is QUIT:
				pygame.quit()
				exit()
			if e.type is MOUSEBUTTONDOWN:
				pygame.quit()
				exit()

	def getPlayerInput(self, board, current_color):
		print(current_color)
		fromSquare = 0
		toSquare = 0
		while not fromSquare or not toSquare:
			squareClicked = []
			for e in pygame.event.get():
				if e.type is KEYDOWN:
					if e.key is K_ESCAPE:
						fromSquare = []
						fromTuple = []
				if e.type is MOUSEBUTTONDOWN:
					(mouseX, mouseY) = pygame.mouse.get_pos()
					print((mouseX,mouseY))
					squareClicked = self.screenToBoard((mouseX,mouseY))
					print(board[squareClicked[0]][squareClicked[1]])
					if squareClicked[0] > 7 or squareClicked[0] < 0 or squareClicked[1] > 7 or squareClicked[1] < 0:
						squareClicked = []
				if e.type is QUIT:
					pygame.quit()
					exit()
			if not fromSquare and not toSquare:
				self.draw(board)
				if squareClicked != []:
					r,c = squareClicked
					if current_color == 'BLACK' and 'b' == board[r][c][0] or \
					   current_color == 'WHITE' and 'w' == board[r][c][0]:
						if len(self.rules.getValidMoves(board, current_color, squareClicked, self.orientation)) > 0:
							fromSquare = 1
							fromTuple = squareClicked
			elif fromSquare and not toSquare:
				possibleMoves = self.rules.getValidMoves(board, current_color, fromTuple, self.orientation)
				self.draw(board, possibleMoves)
				if squareClicked != []:
					r,c = squareClicked
					if squareClicked in possibleMoves:
						toSquare = 1
						toTuple = squareClicked
					elif current_color == 'BLACK' and 'b' == board[r][c][0] or \
					     current_color == 'WHITE' and 'w' == board[r][c][0]:
						if squareClicked == fromTuple:
							fromSquare = 0
						elif len(self.rules.getValidMoves(board,current_color,squareClicked, self.orientation)) > 0:
							fromSquare = 1
							fromTuple = squareClicked
						else:
							fromSquareChosen = 0 #piece is of own color, but no possible moves
					else:
						fromSquare = 0
		return (fromTuple, toTuple)

if __name__ == "__main__":
	g = Game()
	b = Board('WHITE').getState()
	g.draw(b)