import pygame
import random
import math
from pygame import mixer

import sys
import os
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# datas=[('background.png','./'),('background.wav','./'),('bullet.png','./'),('missile.png','./'),('enemy1.png','./'),('explosion.wav','./'),('laser.wav','./'),('player1.png','./'),('ufo.png','./'),('freesansbold.ttf','./')]


# Global variables
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
ENEMYTYPES = 1
PLAYERTYPES = 2
num_players = min(2, int(input('Enter number of players: ')))
deltaP = 0.8
deltaE = 0.2
deltaB = 4
deltaEB = 0.3
textX = 10
textY = 10
# Initialize pygame and Create Screen (or Window)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Images
playerImg = [pygame.image.load(resource_path("player"+str(i+1)+".png")) for i in range(PLAYERTYPES)]
enemyImg = [pygame.image.load(resource_path("enemy"+str(i+1)+".png")) for i in range(ENEMYTYPES)]
bulletImg = [pygame.image.load(resource_path("bullet.png")), pygame.image.load(resource_path("missile.png"))]
# Fonts
font = pygame.font.Font(resource_path("freesansbold.ttf"), 32)
game_over_font = pygame.font.Font(resource_path("freesansbold.ttf"), 64)
# Sounds
EXPLOSION = mixer.Sound(resource_path('explosion.wav'))
LASER = mixer.Sound(resource_path('laser.wav'))
# Background and icon
background = pygame.image.load(resource_path("background.png"))
icon = pygame.image.load(resource_path("ufo.png"))

def show_score(x, y, player):
    sc = font.render("Score: "+str(10*player.score), True, (255,255,255))
    screen.blit(sc, (x, y))

def draw(image, x, y):
    # Draw Image
    screen.blit(image, (x, y))

def drawObj(obj):
    screen.blit(obj.image, (obj.x, obj.y))

def isCollision(a, b, collisionParam):
    dist = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    if dist < collisionParam:
        return True
    return False

def shoot(bullet):
    bullet.dy = bullet.delta
    if bullet.state==0:
        bullet.state = 1
        LASER.play()

def getX(i):
    return SCREEN_WIDTH*(3/4-i/2)-64

class Bullet:
    def __init__(self, x, y, delta, image, parent):
        self.image = image
        self.x = x
        self.y = y
        self.delta = delta
        self.dx = 0
        self.dy = 0
        self.state = 0 # Ready to fire
        self.parent = parent

class Player:
    def __init__(self, x, y, delta, image):
        self.image = image
        self.x = x
        self.y = y
        self.delta = delta
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.bullet = Bullet(self.x, self.y, -deltaB, bulletImg[0],self)
        self.GAMEOVER = False
        
class Enemy:
    def __init__(self, x, y, dx, delta):
        self.image = random.choice(enemyImg)
        self.x = x
        self.y = y
        self.delta = delta
        self.dx = dx
        self.bullet = Bullet(self.x, self.y, deltaEB, bulletImg[1], self)

class Game:
    def __init__(self):
        self.enemy_dy = 70*deltaE
        self.score = 0
        self.GAMEOVER = False
        self.GAMESTATE = 1 # not paused
        # Title and Icon of pygame window
        pygame.display.set_caption("Space War")
        pygame.display.set_icon(icon)
        # Background Music
        mixer.music.load(resource_path('background.wav'))
        mixer.music.play(-1) # -1 means play infinitely
        self.players = [Player(getX(i), 0.7*SCREEN_HEIGHT, deltaP, playerImg[i]) for i in range(num_players)]
        self.num_of_enemies = random.randint(6, 10)
        self.enemies = [Enemy(random.randint(3, SCREEN_WIDTH-67), random.randint(0, 0.4*SCREEN_HEIGHT), deltaE*0.6, deltaE) for i in range(self.num_of_enemies)]
        self.bullets = [self.players[i].bullet for i in range(num_players)]
        for enemy in self.enemies:
            self.bullets.append(enemy.bullet)
        running = True
        while running:
            # Fill Color to Screen (R, G, B)
            screen.fill((0, 0, 0))
            draw(background, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.players[0].dx = -self.players[0].delta
                    if event.key == pygame.K_RIGHT:
                        self.players[0].dx = self.players[0].delta
                    if event.key == pygame.K_UP:
                        self.players[0].dy = -self.players[0].delta
                    if event.key == pygame.K_DOWN:
                        self.players[0].dy = self.players[0].delta
                    if (event.key == pygame.K_KP0 or (num_players==1 and event.key == pygame.K_SPACE)) and self.GAMESTATE == 1 and not self.players[0].GAMEOVER:
                        shoot(self.players[0].bullet)
                    if event.key == pygame.K_a and num_players==2:
                        self.players[1].dx = -self.players[1].delta
                    if event.key == pygame.K_d and num_players==2:
                        self.players[1].dx = self.players[1].delta
                    if event.key == pygame.K_w and num_players==2:
                        self.players[1].dy = -self.players[1].delta
                    if event.key == pygame.K_s and num_players==2:
                        self.players[1].dy = self.players[1].delta
                    if event.key == pygame.K_SPACE and num_players==2 and self.GAMESTATE == 1 and not self.players[1].GAMEOVER:
                        shoot(self.players[1].bullet)
                    if event.key == pygame.K_p:
                        self.GAMESTATE = self.GAMESTATE ^ 1
                    if event.key == pygame.K_r and (self.GAMEOVER or self.GAMESTATE == 0):
                        self.reset()
                        break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.players[0].dy = self.players[0].dx = 0
                    if num_players==2 and (event.key == pygame.K_a or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_d):
                        self.players[1].dy = self.players[1].dx = 0
            # Game not paused
            if self.GAMESTATE == 1:
                # Player Movement
                for player in self.players:
                    # Update Player Coordinates
                    player.x += player.dx
                    player.y += player.dy
                    # Prevent going out of screen
                    if player.x < 0:
                        player.x = 0
                    elif player.x > SCREEN_WIDTH-64:
                        player.x = SCREEN_WIDTH-64
                    if player.y < 0:
                        player.y = 0
                    elif player.y > SCREEN_HEIGHT-64:
                        player.y = SCREEN_HEIGHT-64
                    # Enemy Movement
                    for enemy in self.enemies:
                        # Game Over if collsion with player
                        if isCollision(player, enemy, 28) or isCollision(player, enemy.bullet, 28):
                            EXPLOSION.play()
                            player.GAMEOVER = True
                            if self.players[0].GAMEOVER and (num_players==1 or self.players[1].GAMEOVER):
                                for j in self.enemies:
                                    j.y = 2000
                                self.game_over()
                                break
                        if not self.GAMEOVER:
                            # Update Enemy Pos
                            enemy.x += enemy.dx
                            # Prevent going out of screen
                            if enemy.x <= 0:
                                enemy.dx = deltaE*random.randint(4,15)/10
                                enemy.y += self.enemy_dy
                            elif enemy.x >= SCREEN_WIDTH-64:
                                enemy.dx = -deltaE*random.randint(4,15)/10
                                enemy.y += self.enemy_dy
                            if enemy.y < 0:
                                enemy.y = 0
                            elif enemy.y > SCREEN_HEIGHT:
                                enemy.x = random.randint(3, SCREEN_WIDTH-67)
                                enemy.y = random.randint(0, 0.4*SCREEN_HEIGHT)
                # Bullet Movement
                for bullet in self.bullets:
                    if bullet.state == 1: # Being fired
                        bullet.x += bullet.dx
                        bullet.y += bullet.dy
                    else: # Ready to Fire
                        bullet.x = bullet.parent.x
                        bullet.y = bullet.parent.y
                    if bullet.y < 0 or bullet.y > SCREEN_HEIGHT: # Miss (gone out of screen)
                        bullet.x = bullet.parent.x
                        bullet.y = bullet.parent.y
                        bullet.state = 0
                if not self.GAMEOVER:
                    # Collision of bullet and enemy
                    for player in self.players:
                        for enemy in self.enemies:
                            collision = not player.GAMEOVER and isCollision(player.bullet, enemy, 27)
                            if collision:
                                EXPLOSION.play()
                                player.bullet.x = player.x
                                player.bullet.y = player.y
                                player.bullet.state = 0
                                player.score += 1
                                self.score += 1
                                enemy.x = random.randint(3, SCREEN_WIDTH-67)
                                enemy.y = random.randint(0, 0.4*SCREEN_HEIGHT)
                            elif random.randint(0, 25000)==1:
                                shoot(enemy.bullet)
                # Increase Enemy Speed
                self.enemy_dy = min(self.enemy_dy + 0.0005, 80)
                # Show Score
                show_score(SCREEN_WIDTH-120-25*len(str(self.players[0].score)), 10, self.players[0])
                if num_players==2:
                    show_score(10, 10, self.players[1])
                for player in self.players:
                    if not player.GAMEOVER:
                        drawObj(player.bullet)
                        drawObj(player)
                if not self.GAMEOVER:
                    for enemy in self.enemies:
                        if enemy.bullet.state == 1:
                            drawObj(enemy.bullet)
                        drawObj(enemy)
                else:
                    self.game_over()
                # Update Screen
                pygame.display.update()
    def reset(self):
        self.enemy_dy = 70*deltaE
        self.score = 0
        self.GAMEOVER = False
        self.GAMESTATE = 1 # not paused
        self.players = [Player(getX(i), 0.7*SCREEN_HEIGHT, deltaP, playerImg[i]) for i in range(num_players)]
        self.num_of_enemies = random.randint(6, 10)
        self.enemies = [Enemy(random.randint(3, SCREEN_WIDTH-67), random.randint(0, 0.4*SCREEN_HEIGHT), deltaE*0.6, deltaE) for i in range(self.num_of_enemies)]
        self.bullets = [self.players[i].bullet for i in range(num_players)]
        for enemy in self.enemies:
            self.bullets.append(enemy.bullet)

    def game_over(self):
        self.GAMEOVER = True
        sc = font.render("GAME OVER", True, (255,255,255))
        draw(sc, SCREEN_WIDTH/2.85, SCREEN_HEIGHT/2)

game = Game()