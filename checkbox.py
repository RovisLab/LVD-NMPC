import pygame

class Checkbox():
	def __init__(self, x, y, text, checked = False):
		self.screen = pygame.display.get_surface()
		self.checked = checked
		self.text = text

		self.checkboxRect = pygame.Rect(x, y, 15, 15)
		self.crossRect = pygame.Rect(x + 2, y + 2, 11, 11)

		if pygame.font:
			font = pygame.font.Font(None, 22)
			self.textDisp = font.render(self.text, 1, (0, 0, 0))

		self.textRect = self.textDisp.get_rect(x = x + 25, centery = y + 9)
	
	def update(self):
		pygame.draw.rect(self.screen, (0, 0, 0), self.checkboxRect)

		if self.checked:
			pygame.draw.rect(self.screen, (0, 255, 75), self.crossRect)

		self.screen.blit(self.textDisp, self.textRect)

	def onCheckbox(self, point):
		if point[0] >= self.getX() and point[0] <= (self.getX() + 25 + self.textRect.w) and point[1] >= self.getY() and point[1] <= (self.getY() + 15):
			return True
		else:
			return False

	def changeState(self):
		if self.isChecked():
			self.uncheck()
		else:
			self.check()

	def isChecked(self):
		return self.checked

	def check(self):
		self.checked = True

	def uncheck(self):
		self.checked = False

	def getX(self):
		return self.checkboxRect.x

	def getY(self):
		return self.checkboxRect.y

		