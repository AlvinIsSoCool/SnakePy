import pygame
import random
import settings

class Apple(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.size = 8
		self.color = (204, 37, 44) # Cherry Red.

		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))

		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self, dt):
		pass

	def draw(self, surface):
		radius = self.size // 2
		center_x = self.rect.x + radius
		center_y = self.rect.y + radius

		pygame.draw.circle(surface, self.color, (center_x, center_y), radius)