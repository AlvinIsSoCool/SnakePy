import pygame
import random
import settings

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y, grow_pending):
		super().__init__()
		self.game = game

		# Head Properties.
		self.size = 8
		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))

		self.rect = self.image.get_rect(center=(x, y))
		self.color = (0, 150, 255)

		# Snake-specific properties.
		directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
		self.body_segments = []
		self.direction = random.choice(directions)
		self.next_direction = self.direction
		self.move_timer = 0
		self.move_interval = 0.1
		self.grow_pending = grow_pending
		self.position_history = []
		self.history_length = 0

	def update(self, dt, keys):
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if self.direction != (-1, 0):
				self.next_direction = (1, 0)
		elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if self.direction != (1, 0):
				self.next_direction = (-1, 0)
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if self.direction != (0, -1):
				self.next_direction = (0, 1)
		elif keys[pygame.K_w] or keys[pygame.K_UP]:
			if self.direction != (0, 1):
				self.next_direction = (0, -1)

		self.move_timer += dt
		if self.move_timer >= self.move_interval:
			self.move_timer = 0
			old_head_pos = (self.rect.x, self.rect.y)

			# Move head
			self.direction = self.next_direction
			dx, dy = self.direction
			self.rect.x += dx * self.size
			self.rect.y += dy * self.size
			self.wrap_around_head()

			self.position_history.insert(0, old_head_pos)
			if len(self.position_history) > self.history_length:
				self.position_history.pop()

			for i, segment in enumerate(self.body_segments):
				if i < len(self.position_history):
					segment.x, segment.y = self.position_history[i]
					self.wrap_around_segment(segment)

			if self.check_self_collision():
				print("Player died!")
				self.game.kill_game()

			while self.grow_pending > 0:
				# New segment starts at head's old position
				new_segment = pygame.Rect(old_head_pos[0], old_head_pos[1], self.size, self.size)
				self.body_segments.append(new_segment)
				self.grow_pending -= 1
				self.history_length += 1
				self.position_history.append(old_head_pos)

	def wrap_around_head(self):
		if self.rect.left >= settings.WIDTH:
			self.rect.right = 0
		elif self.rect.right <= 0:
			self.rect.left = settings.WIDTH

		if self.rect.top >= settings.HEIGHT:
			self.rect.bottom = 0
		elif self.rect.bottom <= 0:
			self.rect.top = settings.HEIGHT

	def wrap_around_segment(self, segment):
		if segment.left >= settings.WIDTH:
			segment.right = 0
		elif segment.right <= 0:
			segment.left = settings.WIDTH

		if segment.top >= settings.HEIGHT:
			segment.bottom = 0
		elif segment.bottom <= 0:
			segment.top = settings.HEIGHT

	def grow_player(self):
		self.grow_pending += 1

	def check_self_collision(self):
		for segment in self.body_segments:
			if self.rect.colliderect(segment):
				return True

		return False

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)

		for segment in self.body_segments:
			pygame.draw.rect(surface, self.color, segment)