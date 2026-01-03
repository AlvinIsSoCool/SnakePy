import pygame
import random
import settings

class Apple(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.size = 12
		self.color = (0, 255, 0)

		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))

		self.rect = self.image.get_rect(center=(x, y))

	def update(self, dt):
		pass

	def draw(self, surface):
		center_x, center_y = self.rect.center
		radius = self.size // 2
		pygame.draw.circle(surface, self.color, (center_x, center_y), radius)