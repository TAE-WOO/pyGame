# -*- coding:utf-8 -*-
import pygame, math, random, sys
# import math
# import random

pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
player_pos = [100, 100]
accuracy = [0, 0]       # [적을 맞힌 횟수, 화살 발사 횟수]
arrows = []     # [화살 각도, 화살 x좌표, 화살 y좌표]
keys = [False, False, False, False]
shoot_speed = 10
badgers = [[640, 100]]
badTimer = 100
badTimer1 = 0
healthValue = 194
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badgerImg = pygame.image.load("resources/images/badguy.png")
healthBar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameOver = pygame.image.load("resources/images/gameover.png")
youWin = pygame.image.load("resources/images/youwin.png")

hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)    # play(loops=0, start=0.0) -> default
pygame.mixer.music.set_volume(0.25)

running = 1
exitcode = 0

while running:
    badTimer -= 1
    screen.fill(0)
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass, (x*100, y*100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # Set player position and rotation
    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(-mouse_pos[1]+player_pos[1], mouse_pos[0]-player_pos[0])
    player_rot = pygame.transform.rotate(player, angle*(180/math.pi))
    player_rot_pos = (player_pos[0]-player_rot.get_rect().width/2, player_pos[1]-player_rot.get_rect().height/2)
    screen.blit(player_rot, player_rot_pos)

    # Draw arrow
    index = 0
    for bullet in arrows:
        velx = math.cos(bullet[0]) * shoot_speed    # speed is hypotenuse
        vely = math.sin(bullet[0]) * shoot_speed
        bullet[1] += velx
        bullet[2] -= vely

        if bullet[1] > 640 or bullet[1] < -64 or bullet[2] > 480 or bullet[2] < -64:
            arrows.pop(index)
        index += 1

    # arrow rotation
    for projectile in arrows:
        arrow_rot = pygame.transform.rotate(arrow, projectile[0]*(180/math.pi))
        screen.blit(arrow_rot, (projectile[1], projectile[2]))

    # create badgers
    if badTimer == 0:
        badgers.append([640, random.randint(50, 420)])
        badTimer = 100 - badTimer1*2
        if badTimer1 > 35:
            badTimer1 = 30
        else:
            badTimer1 += 5

    # Attack castle
    index = 0
    for badger in badgers:
        badrect = pygame.Rect(badgerImg.get_rect())
        badrect.left = badger[0]
        badrect.top = badger[1]
        if badrect.left < 64:
            hit.play()
            healthValue -= random.randint(5, 20)
            badgers.pop(index)
        badger[0] -= 7

        # check for collisions
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if bullrect.colliderect(badrect):       # colliderect is colltion method
                enemy.play()
                accuracy[0] += 1
                arrows.pop(index1)
                badgers.pop(index)
            index1 += 1

    index += 1

    for badger in badgers:
        screen.blit(badgerImg, badger)

    # Draw clock
    font = pygame.font.Font(None, 24)
    survivedText = font.render(str((90000-pygame.time.get_ticks())//60000)+":"
                               + str((90000-pygame.time.get_ticks())//1000 % 60).zfill(2), True, (0, 0, 0))
    textRect = survivedText.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedText, textRect)

    # Draw healthBar
    screen.blit(healthBar, (5, 5))
    for health1 in range(healthValue):
        screen.blit(health, (health1+8, 8))

    accuracyText = font.render(str(accuracy[0])+"/"+str(accuracy[1]), True, (0, 0, 0))
    accuracyTextRect = accuracyText.get_rect()
    accuracyTextRect.bottomright = (635, 475)
    screen.blit(accuracyText, accuracyTextRect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

        # Move player
        if keys[0]:
            player_pos[1] -= 5
        elif keys[1]:
            player_pos[0] -= 5
        elif keys[2]:
            player_pos[1] += 5
        elif keys[3]:
            player_pos[0] += 5

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            mouse_pos = pygame.mouse.get_pos()
            accuracy[1] += 1
            arrows.append([
                math.atan2(-mouse_pos[1]+(player_rot_pos[1]+32), mouse_pos[0]-(player_rot_pos[0]+26)),
                player_rot_pos[0]+32,
                player_rot_pos[1]+32
            ])

    # Win/Lose check
    if healthValue <= 0:
        running = 0
        exitcode = 1
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 0
    if accuracy[1] != 0:
        accuracyRate = accuracy[0]/accuracy[1]*100.0
    else:
        accuracyRate = 0

#  Win/Lose display
if exitcode == 1:
    pygame.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy : " + format(accuracyRate, ".2f") + "%", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameOver, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy : " + format(accuracyRate, ".2f") + "%", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youWin, (0, 0))
    screen.blit(text, textRect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()