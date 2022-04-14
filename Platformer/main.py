# Main game File
# PACKAGE INSTALLATION REQUIREMENTS: 'pip install pygame'
#Artwork by Kenney.nl
# Happy Tune by http://opengameart.org/users/syncopika
# Yippee by http://opengameart.org/users/snabisch

import settings
from settings import *
import pygame as pg
from sprites import *
import os

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

        self.load_data()



    def load_data(self):
        # load high score
        with open(os.path.join(game_Folder, HS_FILE), 'r+') as f:
            try:
                self.highscore = f.read()
                # return highscore
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(os.path.join(img_Folder, SPRITESHEET))
        self.jump_sound = pg.mixer.Sound(os.path.join(audio_Folder, 'Jump33.wav'))
        self.pow_sound = pg.mixer.Sound(os.path.join(audio_Folder, 'Boost16.wav'))


    def new(self):
        # start a new game
        self.load_data()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        pg.mixer.music.load(os.path.join(audio_Folder, 'happytune.wav'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < hits[0].rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #if player hits a powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.pow_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

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
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-100, -30))

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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(skyBlue)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(os.path.join(audio_Folder, 'Yippee.wav'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(skyBlue)
        self.draw_text(TITLE, 100, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to Jump", 22, WHITE, WIDTH /2, HEIGHT / 2)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: "+str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        pg.mixer.music.load(os.path.join(audio_Folder, 'Yippee.wav'))
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(skyBlue)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: "+ str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > int(self.highscore):
            highscore = self.score
            self.draw_text("New High Score: " + str(self.score), 22, WHITE, WIDTH / 2, 15)
            with open(os.path.join(game_Folder, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(500)

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








g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()




