import math
import pygame
import random
from pygame import mixer
from time import sleep
import os
from datetime import date

# initialize the pygame

pygame.init()


clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 750
score = 0
lives = 3
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
retry = 3
scoreColor = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creating window with 600x600

# background
background = pygame.image.load('Icons/background.jpg').convert_alpha()
# background sound
mixer.music.load('Sounds/background.wav')  # adding the sound with mixer.music.loadù
mixer.music.play(-1)  # allow you to change mode to play sound

# text score
scoreText = "0"
livesText = str(3)
ScoreCount = 0
#pause text
pauseText_font = pygame.font.SysFont('bookantiquagrassetto', 20, bold=True)
pause_text = pauseText_font.render("Game paused, press p to resume or exit quit to main menu", True, (255, 255, 255))

# gameover
gameover_font = pygame.font.SysFont('couriernew', 65, bold=True)
gameover2_font = pygame.font.SysFont('couriernew', 25, bold=True)
icon = pygame.image.load('Icons/snake.png')  # assigning icon to icon variable
pygame.display.set_caption("snake", "snake")  # set caption text in upper of window
pygame.display.set_icon(icon)  # passing icon variable to set_icon.

# Defining color rgb format
color = (255, 255, 50)  # you can insert color with this or directly in .fill()
# player
playerImg = pygame.image.load('Icons/player.png')
playerX = 290
playerY = 500
playerX_change = 0
playerY_change = 0

# lists/arrays to store more enemies  using .append you can add values to those arrays
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 3


runSave = False




for i in range(numEnemies):
    enemyImg.append(pygame.image.load('Icons/enemy.png').convert_alpha())
    enemyX.append(random.randint(0, WIDTH - 60))
    enemyY.append(random.randint(60, HEIGHT - 530))
    enemyX_change.append(0.5)
    enemyY_change.append(0)

    # bulletEnemy
    bulletEnemyImg = pygame.image.load('Icons/bulletEnemy.png')
    bulletEnemyX = 0
    bulletEnemyY = enemyY[i]
    bulletEnemyX_change = 0
    bulletEnemyY_change = 0.2
    bulletEnemyState = "fire"

# bullet   # ready state you can't see bullet on the screen - fire state bullet is currently moving
bulletImg = pygame.image.load('Icons/laser.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 2
bulletState = "ready"



def player(x, y):
    screen.blit(playerImg, (x, y))  # drawing image into screen with .blit


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x, y))

def fireEnemyBullet(x,y):
    global bulletEnemyState
    bulletEnemyState = "fire"
    screen.blit(bulletEnemyImg, (x, y))




# calculating distance from enemy and bullet. using math.pow to elevate to 2 x and y
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distanceBullet = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distanceBullet < 27:
        return True
    else:
        return False


def isAttacked(enemyX, enemyY, playerX, playerY, bulletEnemyX, bulletEnemyY):
    distanceEnemy = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    distanceBulletEnemy = math.sqrt((math.pow(bulletEnemyX - playerX, 2)) + (math.pow(bulletEnemyY - playerY, 2)))
    if distanceEnemy < 20 or distanceBulletEnemy < 27:
        return True
    else:
        return False

def pause():
    loop = 1
    screen.blit(pause_text, (150, 350))
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    loop = 0
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    os.system('python menu.py')
                    quit()
        pygame.display.update()
        #screen.fill((0, 0, 0))
        clock.tick(60)

def GameOver():
    gameover_text = gameover_font.render("GAME OVER!", True, (255, 0, 0))
    gameover_text2 = gameover2_font.render("Press F1 to restart or ESC to quit to main menu", True, (255, 255, 255))
    screen.blit(gameover_text, (200, 350))
    screen.blit(gameover_text2, (60, 450))

healthPack = pygame.image.load('Icons/life.png')
showedPack = False


def SaveScore(s):
    global ScoreCount
    ScoreCount = s
    with open('Players.txt', 'a') as f:
        f.writelines("Score: " + str(ScoreCount)+" Date: "+ str(date.today()) +"\n")
        f.writelines("------------------------------------------------------\n")
        f.close();
    return ScoreCount

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(f"Icons/exp{i}.png")
            img = pygame.transform.scale(img, (100,100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 5
        #speed animation go through
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        # if the animation is complete then reset index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


explosion_group = pygame.sprite.Group()

# Close window on event quit (like quit button)   if you want that something keeps appearing continuously you have to add it inside loop while
running = True
while running:  # everything that happens in this while runnng must be defined above
    screen.fill((0, 0, 0))  # Changing background color
    # adding background image to screen
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont('bahnschrift', 20, bold=False)  # creates a font for text
    scoreMessage = font.render("Score : " + scoreText, 1, scoreColor)  # renders a text value and puts it into scoreText variable
    screen.blit(scoreMessage, (10, 15))  # blit shows text that we created
    healthMessage = font.render("Lives : " + livesText, 1, red)
    screen.blit(healthMessage, (WIDTH - 130, 15))
    explosion_group.draw(screen)
    explosion_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.8
            if event.key == pygame.K_DOWN:
                playerY_change = 0.8
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":  # to make it fire only when state is ready else when is fire it will wait
                    bulletSound = mixer.Sound('Sounds/shooting.mp3')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_p:
                pause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                               playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # stop player moving when reaching position
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH - 60:
        playerX = WIDTH - 60

    if playerY <= 0:
        playerY = 0
    elif playerY >= HEIGHT - 60:
        playerY = HEIGHT - 60

    # checking boundaries for enemy movement
    for i in range(numEnemies):

        if bulletEnemyState is "fire":
            bulletEnemyX = enemyX[i]
            fireEnemyBullet(bulletEnemyX, bulletEnemyY)
            bulletEnemyY += bulletEnemyY_change


        if bulletEnemyY >= HEIGHT:
            bulletEnemyY = enemyY[i]
            bulletEnemyState = "fire"

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyX[i] += enemyX_change[i]
        elif enemyX[i] >= WIDTH - 60:
            enemyX_change[i] = -0.5
            enemyX[i] += enemyX_change[i]
        # if enemyY[i] <= 0:
        #      enemyY_change[i] = 0.5
        #  elif enemyY[i] >= HEIGHT - 60:
        #       enemyY_change[i] = -0.5

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('Sounds/explosion.wav')
            explosionSound.play()
            explosion = Explosion(enemyX[i], enemyY[i])
            explosion_group.add(explosion)
            bulletEnemyY = enemyY[i]
            bulletY = playerY
            enemyX[i] = random.randint(0, WIDTH - 60)
            enemyY[i] = random.randint(60, WIDTH - 630)
            bulletState = "ready"
            score += 1
            scoreText = str(score)
            print("+", score)
            bulletEnemyState = "ready"
            bulletEnemyState = "fire"
        enemy(enemyX[i], enemyY[i], i)  # show enemy

        attacked = isAttacked(enemyX[i], enemyY[i], playerX, playerY,bulletEnemyX, bulletEnemyY)
        if attacked:
            bulletEnemyY = enemyY[i]
            playerX = random.randint(0, WIDTH - 60)
            playerY = HEIGHT - 60
            print("attacked")
            lives -= 1
            livesText = str(lives)
            print("you have,", lives, "remaining")

        if lives <= 0:
            GameOver()
            for i in range(numEnemies):
                enemyX[i] = 2000
                enemyY[i] = 2000
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if runSave is False:
                        SaveScore(score)
                        runSave = True
                    pygame.quit()
                    os.system('python firstGame.py')
                    quit()
                elif event.key == pygame.K_ESCAPE:
                    if runSave is False:
                        SaveScore(score)
                        runSave = True
                    pygame.quit()
                    os.system('python menu.py')
                    quit()



    enemyX += enemyX_change
    enemyY += enemyY_change
    player(playerX, playerY)  # calling function that shows player img



    # bullet movement when fired
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletEnemyState is "fire":

        fireEnemyBullet(bulletEnemyX,bulletEnemyY)
        bulletEnemyY += bulletEnemyY_change

    # reset state when bullet exits window
    if bulletY <= 0:
        bulletY = playerY
        bulletState = "ready"

    # use """ to comment#
    clock.tick(800)
    pygame.display.update()  # updates the display when something changes it has to be called at the bottom of every change
