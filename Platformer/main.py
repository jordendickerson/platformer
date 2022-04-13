# Main game File
# PACKAGE INSTALLATION REQUIREMENTS: 'pip install pygame'
#Artwork by Kenney
import settings
from settings import *
import pygame as pg
from sprites import *

# KNOWN BUGS:
# NONE FOR NOW

#NOTES:
# if editing highscore.txt, do not leave it empty. If you want the high score to be reset, set it to zero.

class Game:
    def __init__(self):

        # setup pygame
        pg.init()
        pg.mixer.init()

        #set font name
        self.font_name = pg.font.match_font(FONT_NAME)

        #set clock
        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.running = True



    def load_data(self):
        # load high score
        with open(os.path.join(game_Folder, HS_FILE), 'r+') as f:
            try:
                highscore = f.read()
                # return highscore
            except:
                highscore = 0
        # load spritesheet image
        spritesheet = Spritesheet(os.path.join(img_Folder, SPRITESHEET))
        return highscore



    def show_start_screen(self):
        cur_highscore = self.load_data()
        self.screen.fill(skyBlue)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to Jump", 22, WHITE, WIDTH /2, HEIGHT / 2)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: "+str(cur_highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()

    def show_go_screen(self):
        cur_highscore = self.load_data()
        if not self.running:
            return
        self.screen.fill(skyBlue)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: "+ str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to exit", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > int(self.load_data()):
            highscore = self.score
            self.draw_text("New High Score: " + str(self.score), 22, WHITE, WIDTH / 2, 15)
            with open(os.path.join(game_Folder, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(cur_highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(skyBlue)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()




g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()




