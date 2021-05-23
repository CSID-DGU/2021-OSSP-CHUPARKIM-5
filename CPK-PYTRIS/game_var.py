import pygame
import operator
from random import *
from pygame.locals import *

pygame.init()

# 게임 기본 ui
class ui_variables:
    # Fonts
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

    # Background colors
    black = (10, 10, 10)  # rgb(10, 10, 10)
    white = (255, 255, 255)  # rgb(255, 255, 255)
    grey_1 = (26, 26, 26)  # rgb(26, 26, 26)
    grey_2 = (35, 35, 35)  # rgb(35, 35, 35)
    grey_3 = (55, 55, 55)  # rgb(55, 55, 55)

    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    t_color_b = [black, cyan, blue, orange, yellow, green, pink, red, black]


# Define
block_size = 17  # Height, width of single block
width = 10  # Board width
height = 20  # Board height
framerate = 30  # Bigger -> Slower

initial_width = 750
initial_height = 600
w = initial_width
h = initial_height
current_rate = 600 / 750


clock = pygame.time.Clock()
screen = pygame.display.set_mode((initial_width, initial_height), RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")


block_size = round(17 * w / 750)
temp = block_size * 22  # 374가 바뀔 부분
w_1 = block_size * 12  # 204가 바뀔 부분
w_2 = (w - temp) / 2  # 188이 바뀔 부분
w_3 = block_size * 10  # 96 + 74가 바뀔 부분
h_2 = (h - temp) / 2  # 113이 바뀔 부분

num_of_disrot = 0  # current number of display rotation

game_key = (  # left, right, soft_drop
    (K_RIGHT, K_LEFT, K_DOWN),
    (K_DOWN, K_UP, K_LEFT),
    (K_LEFT, K_RIGHT, K_UP),
    (K_UP, K_DOWN, K_RIGHT),
)

# Initial values
blink = False
start = False
pause = False
done = False
game_over = False

# Game mode 1,2,3,4(Original Blackout Rotate Dual)
gamemode_1 = False
gamemode_2 = False
gamemode_3 = False
gamemode_4 = False

locx = 0  # for move board left, right (blackout)
locy = 0  # for move board up, down (blackout)

score = 0
level = 1
goal = level * 5
bottom_count = 0
hard_drop = False

dx, dy = 3, 0  # Minos location status
rotation = 0  # Minos rotation status

mino = randint(1, 7)  # Current mino
next_mino = randint(1, 7)  # Next mino

hold = False  # Hold status
hold_mino = -1  # Holded mino

name_location = 0
name = [65, 65, 65]

with open("leaderboard.txt") as f:
    lines = f.readlines()
lines = [line.rstrip("\n") for line in open("leaderboard.txt")]

leaders = {"AAA": 0, "BBB": 0, "CCC": 0}
for i in lines:
    leaders[i.split(" ")[0]] = int(i.split(" ")[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix