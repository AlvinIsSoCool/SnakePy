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

		# Snake-specific properties. Remove the quotes after testing and verifying logic.
		self.body_segments = []
		self.direction = (1, 0)
		self.next_direction = (1, 0)
		self.grow_pending = 2 # Head + one segment in the beginning.
		self.move_timer = 0
		self.move_interval = 0.2
		# Position Histories for the segments.
		self.position_history = []
		self.history_length = 0

	def update(self, dt, keys):
		self.old_rect.center = self.rect.center

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
			# Apply queued direction
			self.direction = self.next_direction
			# Store current position for body to follow
			self.position_history.insert(0, self.rect.center)

			if len(self.position_history) > self.history_length:
				self.position_history.pop()

			# Move head
			dx, dy = self.direction
			self.rect.x += dx * self.size
			self.rect.y += dy * self.size

			self.update_body()
			if self.check_self_collision():
				# Add logic.

			self.rect.clamp_ip(pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT))

	def update_body(self):
		# Create body segments if growing
		while self.grow_pending > 0:
			# New segment starts at head's old position
			new_segment = pygame.Rect(self.rect)
			self.body_segments.append(new_segment)
			self.grow_pending -= 1
			self.history_length += 1

		# Move each body segment to follow the head's path
		for i, segment in enumerate(self.body_segments):
			if i < len(self.position_history):
				segment.center = self.position_history[i]

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