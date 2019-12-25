import pygame
from pygame.locals import *

class TextBox:
	def __init__(self, screen, minx, maxx, miny, maxy):
		"""
		initialize window logistics
		"""
		self.screen = screen
		pygame.font.init()
		self.fontDef = pygame.font.Font(None, 20)

		self.minx = minx
		self.maxx = maxx
		self.miny = miny
		self.maxy = maxy

		self.width = maxx-minx
		self.height = maxy-miny

		(w,h) = self.fontDef.size('A')
		self.lineHeight = h 
		self.maxLines = self.height // self.lineHeight

		self.lines = []

	def addLine(self, newline):
		# Add a line to the text box, removing old ones if full
		if (len(self.lines) + 1 > self.maxLines): self.lines.pop(0)
		self.lines.append(newline)

	def add(self, message):
		w,h = self.fontDef.size(message)
		remainder = ""
		if w > self.width:
			while w > self.width:
				message = message[0:-1]
				remainder = message[-1] + remainder
		self.addLine(message)
		if len(remainder) > 0:
			self.add(remainder)

	def draw(self):
		x = self.minx 
		y = self.miny
		color = (255,255,255)
		antialiasing = 0
		self.screen.fill((100,100,100))
		for line in self.lines:
			render = self.fontDef.render(line, antialiasing, color)
			self.screen.blit(render, (x,y))
			y += self.lineHeight