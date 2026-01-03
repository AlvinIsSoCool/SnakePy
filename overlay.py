import pygame
import settings

class OverlaySystem:
	def __init__(self, surface):
		self.surface = surface
		self.font = pygame.font.Font(None, 25)

	def draw(self, screen):
		screen.blit(self.surface, (0, 0))

	def draw_score(self, game):
		self.surface.fill((0, 0, 0, 0))

		text1 = self.font.render(f"{'Score:':<15}{game.score}", True, (160, 160, 160))
		text2 = self.font.render(f"{'High Score:':<12}{game.high_score}", True, (160, 160, 160))

		rect2 = text2.get_rect()
		rect1 = text1.get_rect(topleft=(settings.WIDTH - rect2.width - 2, 5))
		rect2 = text2.get_rect(topleft=(settings.WIDTH - rect2.width - 2, 25))

		self.surface.blit(text1, rect1)
		self.surface.blit(text2, rect2)