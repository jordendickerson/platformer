# Game Settings
import random
import os

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")

print(img_Folder)

#High score file
HS_FILE = "highscore.txt"

#Spritesheet file
SPRITESHEET = "spritesheet_jumper.png"


# game title
TITLE = "Hop!" #Sets title
FONT_NAME = 'arial'

# screen size
WIDTH = 480 #sets width of screen
HEIGHT = 600 #sets height of screen

# Player Size
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32

#player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game Properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0


# starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]
# clock speed
FPS = 60 #sets frames per second (clock tick)

# difficulty
diff = "Normal" #sets difficulty


# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255, 0)
skyBlue = (135,206,235)
darkBlue = (86, 105, 184)
cfBlue = (100, 149, 237)