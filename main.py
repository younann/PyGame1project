import pygame
import random
import math
from pygame import mixer

# init the pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('background.jpg')

# background music
mixer.music.load('backmusic.mp3')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("Younan First Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('spaceship.png')
playerx = 370
playery = 490
playerx_change = 0
playery_change = 0

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
enemy_number = 6

for i in range(enemy_number):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(25, 150))
    enemyx_change.append(0.5)
    enemyy_change.append(35)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 3
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# gameover
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def showScore(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyimg[index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # setbackground
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            # if event.key == pygame.K_UP:
            #     playery_change = -0.3
            # if event.key == pygame.K_DOWN:
            #     playery_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0
    # player boarding
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736
    playery += playery_change
    if playery <= 0:
        playery = 0
    if playery >= 536:
        playery = 536

    # enemy boarding
    for i in range(enemy_number):
        # gameOver
        if enemyy[i] > 450:
            for j in range(enemy_number):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
            enemyy[i] += enemyy_change[i]
        if enemyx[i] >= 736:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]
            # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = playery
            bullet_state = "ready"
            smash_sound = mixer.Sound('explosion.wav')
            smash_sound.play()
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(25, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet mvmnt
    if bullety <= 0:
        bullety = playery
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    showScore(textX, textY)
    pygame.display.update()
