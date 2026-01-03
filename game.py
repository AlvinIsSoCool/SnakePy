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
		self.overlay = OverlaySystem(pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA).convert_alpha())

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

	def spawn_apple(self):
		'''if (current_time - self.enemy_last_spawn) > self.enemy_spawn_delay:
			speed_multiplier = min(settings.BASE_SPEED + (minutes_played * (settings.SPEED_MULTIPLIER_PROGRESS / 4)), 1.1)
			self.enemy_spawn_delay = max(250, self.enemy_spawn_delay / speed_multiplier)
			enemy = Enemy(random.randint(5, 315), -15, self.theme, elapsed_ms)
			self.all_sprites.add(enemy)
			self.enemies.add(enemy)
			self.enemy_last_spawn = current_time '''
		pass

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

		self.spawn_apple()

		hits = pygame.sprite.spritecollide(self.player, self.apples, False)
		if hits:
			self.score += 1
			if self.score > self.high_score:
				self.high_score = self.score
			self.score_changed = True
			self.player.grow_player()

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