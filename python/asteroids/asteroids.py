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


class GameObject():

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

	def check_collisions(self, gameObjects):
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

	def shoot(self, gameObjects):
		if self.alive == True:
			gameObjects.append(Bullet(self.x, self.y, self.headingX, self.headingY))

	def check_collisions(self, gameObjects):
		for i in range(len(gameObjects)):
			if isinstance(gameObjects[i], Asteroid):
				if self.rect.colliderect(gameObjects[i].rect) == True:
					self.alive = False


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

	def check_collisions(self, gameObjects):
		for i in range(len(gameObjects)):
			if isinstance(gameObjects[i], Asteroid):
				if self.rect.colliderect(gameObjects[i].rect) == True:
					self.alive = False
					gameObjects.extend(gameObjects[i].split_asteroid())
					gameObjects[i].alive = False


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

gameObjects = []
gameObjects.append(player)
for i in range(len(asteroids)):
	gameObjects.append(asteroids.pop())

while True:
	windowSurfaceObj.fill(blackColor)

	for obj in gameObjects:
		obj.check_collisions(gameObjects)
		if obj.alive == False:
			gameObjects.remove(obj)
		obj.update()
		obj.draw(windowSurfaceObj)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_z:
				player.shoot(gameObjects)

	keysPressed = pygame.key.get_pressed()
	if keysPressed[K_ESCAPE]:
		pygame.quit()
		sys.exit()
	if keysPressed[K_LEFT]:
		player.rotate("COUNTERCLOCKWISE")
	elif keysPressed[K_RIGHT]:
		player.rotate("CLOCKWISE")
	if keysPressed[K_UP]:
		player.thrust()

	pygame.display.update()
	DT = fpsClock.tick(60) / 1000