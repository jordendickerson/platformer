# Main game File
# PACKAGE INSTALLATION REQUIREMENTS: 'pip install pygame'
import settings
from settings import *
import pygame as pg
from sprites import *



# setup pygame
pg.init()
pg.mixer.init()

def show_start_screen():
    pass

def show_go_screen():
    pass


def main():
    running = True
    #Create game objects
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()


    # load assets



    # Create Sprite Groups
    all_sprites = pg.sprite.Group()
    platforms_group = pg.sprite.Group()
    enemy_group = pg.sprite.Group()
    player_group = pg.sprite.Group()


    # create enemy objects


    #create player object
    player = Player()

    #create platforms
    p1 = Platform(0, HEIGHT - 40, WIDTH + (PLAYER_WIDTH*2.5), 40)
    p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 /4, 100, 20)

    # add to sprite groups
    all_sprites.add(player, p1, p2)
    platforms_group.add(p1, p2)
    enemy_group.add()
    player_group.add(player)

    #start game loop
    while running:
        # Update clock
        clock.tick(FPS) #makes the clock tick FPS amount every second
        # Process Events
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
            # if the X was clicked
            if event.type == pg.QUIT:
                running = False



        # Update
        all_sprites.update()

        #check for player-platform collision
        hits = pg.sprite.spritecollide(player,platforms_group, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 1


        # Draw (things drawn first are furthest back, things drawn last are closest. like painting.)
        screen.fill(BLACK) #fills screen with cornflower blue
        all_sprites.draw(screen) #draws all sprites on the screen

        pg.display.flip() #flips screen MUST BE THE LAST THING CALLED


main()


