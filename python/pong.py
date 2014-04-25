import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Ponggggg')

blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)

paddleWidth = 10
paddleHeight = 100
leftPaddle = {'x': 10, 'y': 250, 'speed': 0}
rightPaddle = {'x': 780, 'y': 250, 'speed': 0}

ball = {'x': 380.0, 'y': 280.0, 'size': 10, 'speed': 5.0, 'x_direction': 1, 'y_direction': 1}

def updateLocations():
	leftPaddle['y'] += leftPaddle['speed']
	if leftPaddle['y'] < 10:
		leftPaddle['y'] = 10
	if leftPaddle['y'] > 490:
		leftPaddle['y'] = 490
	
	rightPaddle['y'] += rightPaddle['speed']
	if rightPaddle['y'] < 10:
		rightPaddle['y'] = 10
	if rightPaddle['y'] > 490:
		rightPaddle['y'] = 490

	ball['x'] += ball['speed'] * ball['x_direction']
	ball['y'] += ball['speed'] * ball['y_direction']

	ball['speed'] += 0.005

def detectCollisions():
	if ball['y'] <= 10 or ball['y'] >= 580:
		ball['y_direction'] *= -1
	if ball['x_direction'] > 0 and ball['x'] >= 765 and ball['x'] <= 780:
		if rightPaddle['y'] < ball['y'] + 5 and rightPaddle['y'] + paddleHeight > ball['y'] + ball['size'] - 5:
			ball['x_direction'] *= -1
	if ball['x_direction'] < 0 and ball['x'] <= 25 and ball['x'] >= 10:
		if leftPaddle['y'] < ball['y'] + 5 and leftPaddle['y'] + paddleHeight > ball['y'] + ball['size'] - 5:
			ball['x_direction'] *= -1

def doDraw():
	windowSurfaceObj.fill(blackColor)
	
	pygame.draw.rect(windowSurfaceObj, whiteColor, (leftPaddle['x'], leftPaddle['y'], paddleWidth, paddleHeight))
	pygame.draw.rect(windowSurfaceObj, whiteColor, (rightPaddle['x'], rightPaddle['y'], paddleWidth, paddleHeight))
	pygame.draw.rect(windowSurfaceObj, whiteColor, (int(ball['x']), int(ball['y']), ball['size'], ball['size']))

def getInput():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_s:
				leftPaddle['speed'] = 15
			if event.key == K_w:
				leftPaddle['speed'] = -15
			if event.key == K_k:
				rightPaddle['speed'] = 15
			if event.key == K_o:
				rightPaddle['speed'] = -15
		if event.type == KEYUP:
			if event.key in (K_s, K_w):
				leftPaddle['speed'] = 0
			if event.key in (K_k, K_o):
				rightPaddle['speed'] = 0
			if event.key == K_r:
				ball['x'] = 380.0
				ball['y'] = 280.0
				ball['speed'] = 5.0

while True:

	detectCollisions()
	updateLocations()
	doDraw()
	getInput()

	pygame.display.update()
	fpsClock.tick(60)