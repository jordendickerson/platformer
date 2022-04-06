# Game Settings
import random
import os

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")
print(img_Folder)



# game title
TITLE = "Platformer" #Sets title

# screen size
WIDTH = 480 #sets width of screen
HEIGHT = 600 #sets height of screen

# Player Size
PLAYER_HEIGHT = WIDTH // 10
PLAYER_WIDTH = WIDTH // 10

#player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12

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
cfBlue = (100, 149, 237)