import pygame
import settings

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.size = 8
		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))

		self.rect = self.image.get_rect(center=(x, y))
		self.old_rect = self.rect.copy()
		self.color = (0, 150, 255)
		self.speed = 200

	def update(self, dt, keys):
		self.old_rect.center = self.rect.center

		dx = dy = 0
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			dx = 1
		elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
			dx = -1
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
			dy = 1
		elif keys[pygame.K_w] or keys[pygame.K_UP]:
			dy = -1

		if dx == 0 and dy == 0:
			return

		if dx != 0:
			self.rect.x += dx * self.speed * dt
		elif dy != 0:
			self.rect.y += dy * self.speed * dt

		self.rect.clamp_ip(pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT))

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)

	def grow_player():
		pass