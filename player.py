class Player:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.type = 'Player'
	def getName(self):
		return self.name 
	def getColor(self):
		return self.color 
	def getType(self):
		return self.type