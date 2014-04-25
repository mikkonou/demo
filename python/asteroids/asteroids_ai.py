from __future__ import division
import pygame, sys, math, random
from pygame.locals import *

WINDOWSIZE = 800
DT = 1

SHIPMAXSPEED = 600.0
SHIPACCELERATIONRATE = 400.0
SHIPTURNINGRATE = 400.0
SHIPIMAGESIZE = 20

BULLETSPEED = 800.0
BULLETTIMETOLIVE = 300.0
BULLETRATEOFFIRE = 3
BULLETDELAY = 1000 / BULLETRATEOFFIRE

THRUSTDELAY = 300

ASTEROIDLARGEBASESPEED = 100.0
ASTEROIDMEDIUMBASESPEED = 200.0
ASTEROIDSMALLBASESPEED = 400.0
ASTEROIDSPEEDVARIANCE = 30.0
ASTEROIDANGLEVARIANCE = 60.0
ASTEROIDROTATIONSPEEDVARIANCE = 10

LARGE = 1
MEDIUM = 2
SMALL = 3

blackColor = pygame.Color(0, 0, 0)
random.seed()


class GameObject(object):

	def update(self):
		self.x += self.speedX * DT
		self.y += self.speedY * DT
		self.rect.center = (self.x, self.y)

		if self.x < 0:
			self.x = WINDOWSIZE
		elif self.x > WINDOWSIZE:
			self.x = 0
		if self.y < 0:
			self.y = WINDOWSIZE
		elif self.y > WINDOWSIZE:
			self.y = 0

	def draw(self, surface):
		oldRect = self.entityImage.get_rect(center = (int(self.x), int(self.y)))
		oldCenter = oldRect.center
		sprite = pygame.transform.rotate(self.entityImage, self.angle)
		rotatedRect = sprite.get_rect()
		rotatedRect.center = oldCenter
		surface.blit(sprite, rotatedRect)

	def check_collisions(self, game_objects):
		pass


class Ship(GameObject):

	def __init__(self):
		self.x, self.y = WINDOWSIZE / 2.0, WINDOWSIZE / 2.0
		self.angle = 0.0
		self.headingX = 0.0
		self.headingY = -1.0
		self.speedX = 0.0
		self.speedY = 0.0
		self.entityImage = pygame.transform.scale(pygame.image.load("ship.png"), (SHIPIMAGESIZE, SHIPIMAGESIZE))
		self.entityImage.set_colorkey(blackColor)
		self.rect = pygame.Rect(self.x, self.y, self.entityImage.get_rect().width, self.entityImage.get_rect().height)
		self.alive = True
		self.bullet_time = 0
		self.thrust_time = 0

	def rotate(self, direction):
		if direction == "COUNTERCLOCKWISE":
			self.angle += SHIPTURNINGRATE * DT
		if direction == "CLOCKWISE":
			self.angle -= SHIPTURNINGRATE * DT
		
		if self.angle > 360.0:
			self.angle -= 360.0
		if self.angle < 0.0:
			self.angle += 360.0

		self.headingX = math.cos(math.radians(self.angle + 90))
		self.headingY = -math.sin(math.radians(self.angle + 90))

	def thrust(self):
		self.speedX += self.headingX * SHIPACCELERATIONRATE * DT
		self.speedY += self.headingY * SHIPACCELERATIONRATE * DT
		self.rect.center = (self.x, self.y)

		if self.speedX > SHIPMAXSPEED:
			self.speedX = SHIPMAXSPEED
		if self.speedX < -SHIPMAXSPEED:
			self.speedX = -SHIPMAXSPEED
		if self.speedY > SHIPMAXSPEED:
			self.speedY = SHIPMAXSPEED
		if self.speedY < -SHIPMAXSPEED:
			self.speedY = -SHIPMAXSPEED

	def shoot(self, game_objects):
		if self.alive == True:
			current_time = pygame.time.get_ticks()
			if self.bullet_time + BULLETDELAY < current_time:
				game_objects.append(Bullet(self.x, self.y, self.headingX, self.headingY))
				self.bullet_time = current_time

	def check_collisions(self, game_objects):
		for i in range(len(game_objects)):
			if isinstance(game_objects[i], Asteroid):
				if self.rect.colliderect(game_objects[i].rect) == True:
					self.alive = False

	def get_distance(self, asteroid):
		return math.sqrt(math.pow(asteroid.x - self.x, 2) + pow(asteroid.y - self.y, 2))

	def find_nearest(self, game_objects):
		distance_to_nearest = 10000.0
		nearest = None
		for o in game_objects:
			if type(o) == Asteroid:
				distance = self.get_distance(o)
				if distance < distance_to_nearest:
					distance_to_nearest = distance
					nearest = o
		return nearest

	def turn_towards_asteroid(self, asteroid):
		angle = math.degrees(math.atan2(asteroid.y - self.y, asteroid.x - self.x)) + 180
		self.angle = -angle + 90
		self.headingX = math.cos(math.radians(self.angle + 90))
		self.headingY = -math.sin(math.radians(self.angle + 90))

	def shoot_if_in_range(self, game_objects, asteroid):
		if self.get_distance(asteroid) < 300:
			self.shoot(game_objects)
		else:
			current_time = pygame.time.get_ticks()
			if self.thrust_time + THRUSTDELAY < current_time:
				self.thrust()
				self.thrust_time = current_time

	def ai(self, game_objects):
		#find nearest
		#turn towards nearest
		#check range
		#if in range, shoot
		#else, accelerate
		#shoot
		#repeat
		pass

class Bullet(GameObject):

	def __init__(self, x, y, headingX, headingY):
		self.x, self.y = x, y
		self.headingX, self.headingY = headingX, headingY
		self.speedX = BULLETSPEED * self.headingX
		self.speedY = BULLETSPEED * self.headingY
		self.timeCreated = pygame.time.get_ticks()
		self.entityImage = pygame.image.load("bullet.png")
		self.rect = pygame.Rect(self.x, self.y, self.entityImage.get_rect().width, self.entityImage.get_rect().height)
		self.alive = True

	def update(self):
		self.x += self.speedX * DT
		self.y += self.speedY * DT
		self.rect.center = (self.x, self.y)

		if self.x < 0:
			self.x = WINDOWSIZE
		elif self.x > WINDOWSIZE:
			self.x = 0
		if self.y < 0:
			self.y = WINDOWSIZE
		elif self.y > WINDOWSIZE:
			self.y = 0

		if pygame.time.get_ticks() - self.timeCreated > BULLETTIMETOLIVE:
			self.alive = False

	def draw(self, surface):
		surface.blit(self.entityImage, (self.x, self.y))

	def check_collisions(self, game_objects):
		for i in range(len(game_objects)):
			if isinstance(game_objects[i], Asteroid):
				if self.rect.colliderect(game_objects[i].rect) == True:
					self.alive = False
					game_objects.extend(game_objects[i].split_asteroid())
					game_objects[i].alive = False


class Asteroid(GameObject):

	def __init__(self, x, y, rotationSpeed, angle, direction, size):
		self.x, self.y = x, y
		self.speedX = ASTEROIDLARGEBASESPEED - random.random() * ASTEROIDSPEEDVARIANCE
		self.speedY = ASTEROIDLARGEBASESPEED - random.random() * ASTEROIDSPEEDVARIANCE
		self.rotationSpeed = rotationSpeed
		self.angle = angle
		self.direction = direction
		self.size = size
		self.headingX = math.cos(math.radians(self.direction))
		self.headingY = -math.sin(math.radians(self.direction))
		self.entityImage = pygame.image.load("asteroid.png")
		self.entityImage = pygame.transform.scale(self.entityImage, (self.entityImage.get_width() // self.size, self.entityImage.get_height() // self.size))
		self.entityImage.set_colorkey(blackColor)
		self.rect = pygame.Rect(self.x, self.y, self.entityImage.get_rect().width, self.entityImage.get_rect().height)		
		self.alive = True

	@staticmethod
	def create_asteroid(x, y):
		rotationSpeed = random.random() * 2.0
		angle = random.random() * 360.0
		direction = random.random() * 360.0
		return Asteroid(x, y, rotationSpeed, angle, direction, LARGE)

	def split_asteroid(self):
		if self.size != SMALL:
			return [Asteroid(self.x, self.y, self.rotationSpeed, self.angle, self.direction - 20, self.size + 1), \
					Asteroid(self.x, self.y, self.rotationSpeed, self.angle, self.direction + 20, self.size + 1)]
		else: 
			return []

	def update(self):
		self.x += self.speedX * self.headingX * DT
		self.y += self.speedY * self.headingY * DT
		self.rect.center = (self.x, self.y)
		self.angle += self.rotationSpeed

		if self.x < 0:
			self.x = WINDOWSIZE
		elif self.x > WINDOWSIZE:
			self.x = 0
		if self.y < 0:
			self.y = WINDOWSIZE
		elif self.y > WINDOWSIZE:
			self.y = 0


pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
pygame.display.set_caption("Asteroidzzzz")

player = Ship()
asteroids = [Asteroid.create_asteroid(100, 100), Asteroid.create_asteroid(700, 100), Asteroid.create_asteroid(400, 700)]

game_objects = []
game_objects.append(player)
for i in range(len(asteroids)):
	game_objects.append(asteroids.pop())

while True:
	windowSurfaceObj.fill(blackColor)

	for obj in game_objects:
		obj.check_collisions(game_objects)
		if obj.alive == False:
			game_objects.remove(obj)
		obj.update()
		obj.draw(windowSurfaceObj)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	nearest = player.find_nearest(game_objects)
	player.turn_towards_asteroid(nearest)
	player.shoot_if_in_range(game_objects, nearest)

	pygame.display.update()
	DT = fpsClock.tick(60) / 1000