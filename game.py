import pygame
import sys
import random
import settings
import math

from player import Player
from apple import Apple
from overlay import OverlaySystem

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
		pygame.display.set_caption("Snake Game")

		self.fps = settings.FPS
		self.clock = pygame.time.Clock()
		self.running = True

		self.all_sprites = pygame.sprite.Group()
		self.apples = pygame.sprite.Group()

		self.player = Player(settings.WIDTH // 2, settings.HEIGHT // 2)
		self.all_sprites.add(self.player)

		self.game_start_time = pygame.time.get_ticks()
		self.score_changed = True
		self.score = 0
		self.high_score = 0
		self.apple_last_spawn = self.game_start_time
		self.apple_spawn_delay = 750
		self.overlay = OverlaySystem(pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA).convert_alpha())

		self.spawn_apple()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.end_game()

			if event.type == pygame.WINDOWFOCUSLOST or event.type == pygame.WINDOWMINIMIZED:
				self.fps /= 4

			if event.type == pygame.WINDOWFOCUSGAINED or event.type == pygame.WINDOWRESTORED:
				self.fps = settings.FPS

	# Add chance too, maybe?
	def spawn_apple(self):
		for apple in self.apples:
			apple.kill()

		snake_positions = []
		snake_positions.append(self.player.rect.topleft)

		for segment in self.player.body_segments:
			snake_positions.append(segment.topleft)

		max_attempts = 10
		for _ in range(max_attempts):
			grid_size = self.player.size
			x = random.randrange(0, settings.WIDTH - grid_size, grid_size)
			y = random.randrange(0, settings.HEIGHT - grid_size, grid_size)

			position_free = True
			for pos in snake_positions:
				if (x, y) == pos:
					position_free = False
					break

			if position_free:
				apple = Apple(x, y)
				self.all_sprites.add(apple)
				self.apples.add(apple)
				return

		print("No position found!")

	def update(self, dt):
		if not self.running:
			return
		keys = pygame.key.get_pressed()

		for sprite in self.all_sprites:
			if hasattr(sprite, 'update'):
				if sprite == self.player:
					sprite.update(dt, keys)
				else:
					sprite.update(dt)

		hits = pygame.sprite.spritecollide(self.player, self.apples, True)
		for apple in hits:
			self.score += 1

			if self.score > self.high_score:
				self.high_score = self.score

			self.score_changed = True
			self.player.grow_player()

		current_time = pygame.time.get_ticks()
		if (current_time - self.apple_last_spawn) > self.apple_spawn_delay:
			self.spawn_apple()
			self.apple_last_spawn = current_time

	def draw(self):
		self.screen.fill((10, 10, 10))

		for sprite in self.all_sprites:
			if hasattr(sprite, 'draw'):
				sprite.draw(self.screen)

		if self.score_changed:
			self.overlay.draw_score(self)
			self.score_changed = False

		self.overlay.draw(self.screen)
		pygame.display.flip()

	def end_game(self):
		self.running = False

	def run(self):
		while self.running:
			dt = min(1/10, self.clock.tick(self.fps) / 1000)
			self.handle_events()
			self.update(dt)
			self.draw()

		pygame.quit()
		sys.exit()