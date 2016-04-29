# -*- coding:utf-8 -*-
import pygame
import math
import random

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
player_pos = [100, 100]
accuracy = [0, 0]       # [적을 맞힌 횟수, 화살 발사 횟수]
arrows = []     # [화살 각도, 화살 x좌표, 화살 y좌표]
keys = [False, False, False, False]
badguys = [[640, 100]]
badtimer = 100
badtimer1 = 0
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg = pygame.image.load("resources/images/badguy.png")

while True:
    screen.fill(0)
    badtimer -= 1
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass, (x*100, y*100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(-mouse_pos[1]+player_pos[1], mouse_pos[0]-player_pos[0])
    player_rot = pygame.transform.rotate(player, angle*(180/math.pi))
    player_rot_pos = (player_pos[0]-player_rot.get_rect().width/2, player_pos[1]-player_rot.get_rect().height/2)
    screen.blit(player_rot, player_rot_pos)

    index = 0
    for bullet in arrows:
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] -= vely

        if bullet[1] > 640 or bullet[1] < -64 or bullet[2] > 480 or bullet[2] < -64:
            arrows.pop(index)
        index += 1

    for projectile in arrows:
        arrow_rot = pygame.transform.rotate(arrow, projectile[0]*(180/math.pi))
        screen.blit(arrow_rot, (projectile[1], projectile[2]))

    if badtimer == 0:
        badguys.append([640, random.randint(50, 420)])
        badtimer = 100 - badtimer1*2
        if badtimer1 > 35:
            badtimer1 = 30
        else:
            badtimer1 += 5

    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= 7

    index += 1

    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
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

        if keys[0]:
            player_pos[1] -= 5
        elif keys[1]:
            player_pos[0] -= 5
        elif keys[2]:
            player_pos[1] += 5
        elif keys[3]:
            player_pos[0] += 5

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            accuracy[1] += 1
            arrows.append([
                math.atan2(-mouse_pos[1]+(player_rot_pos[1]+32), mouse_pos[0]-(player_rot_pos[0]+26)),
                player_rot_pos[0]+32,
                player_rot_pos[1]+32
            ])