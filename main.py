import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption("Way2Back")

WINDOW_SIZE = (400, 400)
#define
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player_image = pygame.image.load('images/player.png')

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_height(), player_image.get_width())
test_rect = pygame.Rect(100,100,100,50) # bu sayilarin anlami = (x,y,uzun kenar, kisa kenar)

while True:
    screen.fill((146,244,255))

    screen.blit(player_image, player_location)

    if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect) #parantez icinin anlami (Ekrani (renk) boyancak cisim(Rect) )
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: #yurumek icin
            if event.key == K_RIGHT: #tusu soyluyon
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP: #keyup dedigi iste tusa basili tutmaktan kaldiriyon ya o
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    pygame.display.update()
    clock.tick(60)