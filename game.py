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
		pygame.display.set_caption("Snake 1.0.0")

		self.fps = settings.FPS
		self.clock = pygame.time.Clock()
		self.running = True

		self.all_sprites = pygame.sprite.Group()
		self.apples = pygame.sprite.Group()

		self.player = Player(self, settings.WIDTH // 2, settings.HEIGHT // 2, grow_pending=4) # Spawn with an initial length.
		self.all_sprites.add(self.player)

		self.game_start_time = pygame.time.get_ticks()
		self.score_changed = True
		self.score = 0
		self.high_score = self.score
		self.apple_last_spawn = self.game_start_time
		self.apple_spawned = False
		self.apple_spawn_delay = 1500
		self.overlay = OverlaySystem(pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA))

		# Spawn the initial apple.
		self.spawn_apple(self.game_start_time, force=True)

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.kill_game()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.kill_game()

			active = self.is_window_active(event)
			if active is not None:
				if active:
					self.fps = settings.FPS
				else:
					self.fps = 15

	def is_window_active(self, event):
		if hasattr(pygame, 'WINDOWFOCUSLOST'):
			if event.type == pygame.WINDOWFOCUSGAINED or event.type == pygame.WINDOWRESTORED:
				return True
			elif event.type == pygame.WINDOWFOCUSLOST or event.type == pygame.WINDOWMINIMIZED:
				return False
		elif event.type == pygame.ACTIVEEVENT:
			if event.state == 1:
				if event.gain == 1:
					return True # Mouse entry.
			elif event.state == 2 and event.gain == 0:
				return False # Focus loss.
		elif event.type == pygame.VIDEOEXPOSE:
			return True # Window Repaint.
		else:
			return None

	def spawn_apple(self, current_time, force=False):
		# 35% Chance for apple to spawn.
		if (not self.apple_spawned and random.random() < 0.35) or force:
			snake_positions = []
			snake_positions.append(self.player.rect.topleft)

			for segment in self.player.body_segments:
				snake_positions.append(segment.topleft)

			max_attempts = 3
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
					self.apple_spawned = True
					return

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
			self.change_player_length()
			self.apple_spawned = False

		current_time = pygame.time.get_ticks()
		if (current_time - self.apple_last_spawn) > self.apple_spawn_delay:
			self.spawn_apple(current_time)
			self.apple_last_spawn = current_time

	def change_player_length(self):
		self.score += 1

		if self.score > self.high_score:
			self.high_score = self.score

		self.score_changed = True
		self.player.grow_player()

	def draw(self):
		self.screen.fill((5, 5, 5))

		for sprite in self.all_sprites:
			if hasattr(sprite, 'draw'):
				sprite.draw(self.screen)

		if self.score_changed:
			self.overlay.draw_score(self)
			self.score_changed = False

		self.overlay.draw(self.screen)
		pygame.display.flip()

	def kill_game(self):
		self.running = False

	def run(self):
		while self.running:
			dt = min(1.0 / 10.0, self.clock.tick(self.fps) / 1000.0)
			self.handle_events()
			self.update(dt)
			self.draw()

		pygame.quit()
		sys.exit()