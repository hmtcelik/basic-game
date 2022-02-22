import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption("my first game")

WINDOW_SIZE = (800, 520)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((300, 200))

player_image = pygame.image.load('images/player.png')
player_image.set_colorkey((255,255,255))      # remove white color background on your character

grass_image = pygame.image.load("images/grasstile.png")
dirt_image = pygame.image.load("images/tiledirt.png")
coin_image = pygame.image.load("images/coin.png")
tree_image = pygame.image.load("images/tree.png")
left_bottom_dirt = pygame.image.load("images/dirttilebottomleft.png")
right_bottom_dirt = pygame.image.load("images/dirttilebottomright.png")
right_dirt = pygame.image.load("images/dirttilerightt.png")
left_dirt = pygame.image.load("images/dirttileleft.png")
bottom_dirt = pygame.image.load("images/dirttilebottom.png")


TILE_SIZE = grass_image.get_width()

def load_map(path):
    f = open(path + '.txt' , 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]


player_rect = pygame.Rect(50,50, player_image.get_height(), player_image.get_width())
test_rect = pygame.Rect(150,150,100,50) # meaning = (x, y, long side, short side)

while True:
    display.fill((146,244,255)) #background color

    true_scroll[0] += (player_rect.x-true_scroll[0]-150)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 80)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)



    #fill object on your game
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '3':
                display.blit(left_bottom_dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '4':
                display.blit(right_bottom_dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '5':
                display.blit(right_dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '6':
                display.blit(left_dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '7':
                display.blit(bottom_dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))

            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] += -2
    player_movement[1] = player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)\

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: #for walking (keydown is when you press a button on keybord)
            if event.key == K_RIGHT: #k_right meaning = right key (just on keybord)
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_d: # k_d meaning just button d on keybord
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 20:
                    player_y_momentum = -5
            if event.key == K_w:
                if air_timer < 20:
                    player_y_momentum = -5
        if event.type == KEYUP: #keyup = when you break; pressing button on keybord so key up
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(60) #60 fps