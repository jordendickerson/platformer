# Main game File
# PACKAGE INSTALLATION REQUIREMENTS: 'pip install pygame'
import settings
from settings import *
import pygame as pg
from sprites import *

#CURRENT BUGS: High score will not read, but will write.



# setup pygame
pg.init()
pg.mixer.init()

#set font name
font_name = pg.font.match_font(FONT_NAME)

#set clock
clock = pg.time.Clock()

def load_data():
    #load high score
    with open(os.path.join(game_Folder, HS_FILE), 'w') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
    return highscore

def show_start_screen(surf):
    cur_highscore = str(load_data())
    surf.fill(skyBlue)
    draw_text(surf, TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text(surf, "Arrows to move, Space to Jump", 22, WHITE, WIDTH /2, HEIGHT / 2)
    draw_text(surf, "Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
    draw_text(surf, "High Score: "+cur_highscore, 22, WHITE, WIDTH / 2, 15)
    pg.display.flip()
    waitForKey()

def show_go_screen(surf, score, running):
    if not running:
        return
    surf.fill(skyBlue)
    draw_text(surf, "GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text(surf, "Score: "+ str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text(surf, "Press any key to exit", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    if score > load_data():
        highscore = score
        draw_text(surf, "New High Score: " + str(load_data()), 22, WHITE, WIDTH / 2, 15)
        with open(os.path.join(game_Folder, HS_FILE), 'w') as f:
            f.write(str(score))
    else:
        draw_text(surf, "High Score: " + str(load_data()), 22, WHITE, WIDTH / 2, 15)
    pg.display.flip()
    waitForKey()

def waitForKey():
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            if event.type == pg.KEYUP:
                waiting = False


def draw_text(surf, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



def main():
    # set score
    score = 0

    # Create game objects
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)

    show_start_screen(screen)
    running = True

    load_data()



    # load assets



    # Create Sprite Groups
    all_sprites = pg.sprite.Group()
    platforms_group = pg.sprite.Group()
    enemy_group = pg.sprite.Group()
    player_group = pg.sprite.Group()


    # create enemy objects

    # create platforms
    for plat in PLATFORM_LIST:
        p = Platform(*plat)
        all_sprites.add(p)
        platforms_group.add(p)


    #create player object
    player = Player()



    # add to sprite groups
    all_sprites.add(player)
    player_group.add(player)
    platforms_group.add()
    enemy_group.add()


    #start game loop
    while running:
        # Update clock
        clock.tick(FPS) #makes the clock tick FPS amount every second
        # Process Events
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_SPACE or event.key == pg.K_w:
                    hits = pg.sprite.spritecollide(player, platforms_group, False)
                    if hits:
                        player.jump()
            # if the X was clicked
            if event.type == pg.QUIT:
                running = False



        # Update
        all_sprites.update()

        #check for player-platform collision - only if falling
        if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player,platforms_group, False)
            if hits:
                player.pos.y = hits[0].rect.top
                player.vel.y = 0

        # if player reaches top 1/4 of screen
        if player.rect.top <= HEIGHT / 4:
            player.pos.y += abs(player.vel.y)
            for plat in platforms_group:
                plat.rect.y += abs(player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    score += 10

        # span new platforms to keep same average number
        while len(platforms_group) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH-width), random.randrange(-75, -30), width, 20)
            platforms_group.add(p)
            all_sprites.add(p)

        # Die!
        if player.rect.bottom > HEIGHT:
            for sprite in all_sprites:
                sprite.rect.y -= max(player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(platforms_group) == 0:
            # show game over screen
            show_go_screen(screen, score, running)
            running = False


        # Draw (things drawn first are furthest back, things drawn last are closest. like painting.)
        screen.fill(skyBlue) #fills screen with cornflower blue
        all_sprites.draw(screen) #draws all sprites on the screen
        draw_text(screen, str(score), 22, WHITE, WIDTH / 2, 50)

        pg.display.flip() #flips screen MUST BE THE LAST THING CALLED




main()


