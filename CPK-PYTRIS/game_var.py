import pygame
import operator
from random import *
from pygame.locals import *

pygame.init()

# Define
block_size = 17  # Height, width of single block
width = 10  # Board width
height = 20  # Board height
framerate = 30  # Bigger -> Slower

initial_width = 750
initial_height = 600
w = initial_width
h = initial_height
minimum_width = 500
minimum_height = 400
current_rate = 600 / 750

clock = pygame.time.Clock()
screen = pygame.display.set_mode((initial_width, initial_height), RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("CPKTIRS!™")


block_size = round(17 * w / 750)
temp = block_size * 22  # 374가 바뀔 부분
w_1 = block_size * 12  # 204가 바뀔 부분
w_2 = (w - temp) / 2  # 188이 바뀔 부분
w_3 = block_size * 10  # 96 + 74가 바뀔 부분
h_1 = (h - temp) / 2  # 113이 바뀔 부분

img_w = w_2 + temp
img_h = h_1 + temp

w_d1_2 = (w - temp) /5
w_d2_2 = (w - temp) /1.3

num_of_disrot = 0  # current number of display rotation

game_key = (  # left, right, soft_drop
    (K_RIGHT, K_LEFT, K_DOWN),
    (K_DOWN, K_UP, K_LEFT),
    (K_LEFT, K_RIGHT, K_UP),
    (K_UP, K_DOWN, K_RIGHT),
)

# 게임 기본 ui
class ui_variables:
    # Fonts
    font_path = "./assets/fonts/DungGeunMo.ttf"
    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

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
    red_b = (255, 0, 0) # rgb(255, 0, 0)

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


# Image
background_image = "assets/images/retrotv.jpg"
main_image = "assets/images/main.png"
pause_image = "assets/images/pause.jpg"
info_image = "assets/images/info.jpg"
howtoplay_image = "assets/images/howtoplay.png"
main = pygame.image.load(main_image)
main = pygame.transform.scale(main, (initial_width, initial_height))
background = pygame.image.load(background_image)
background = pygame.transform.scale(background, (initial_width, initial_height))
pau = pygame.image.load(pause_image)
pau = pygame.transform.scale(pau, (initial_width, initial_height))
info = pygame.image.load(info_image)
info = pygame.transform.scale(info, (initial_width, initial_height))
howtoplay = pygame.image.load(howtoplay_image)
howtoplay = pygame.transform.scale(howtoplay, (initial_width, initial_height))

# Objects
text1 = ui_variables.h2.render("original", 1, ui_variables.white)
text2 = ui_variables.h2.render("original", 1, ui_variables.red)
text3 = ui_variables.h2.render("blackout", 1, ui_variables.white)
text4 = ui_variables.h2.render("blackout", 1, ui_variables.red)
text5 = ui_variables.h2.render("rotate", 1, ui_variables.white)
text6 = ui_variables.h2.render("rotate", 1, ui_variables.red)
text7 = ui_variables.h2.render("dual screen", 1, ui_variables.white)
text8 = ui_variables.h2.render("dual screen", 1, ui_variables.red)
text9 = ui_variables.h2.render("information", 1, ui_variables.white)
text10 = ui_variables.h2.render("information", 1, ui_variables.red)
text11 = ui_variables.h2.render("sound on", 1, ui_variables.red)
text12 = ui_variables.h2.render("sound off", 1, ui_variables.red)
text13 = ui_variables.h2.render("Return to Main Screen", 1, ui_variables.white)
text14 = ui_variables.h2.render("Return to Main Screen", 1, ui_variables.red)
pause_start = ui_variables.h2.render(
                "(Press esc to continue)", 1, ui_variables.white
            )
rectangle = (0, 10, 100, 100)

# Initial values
blink = False
start = False
pause = False
done = False
game_over = False
popup = False

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


class game_loc:  # ui 위치 비율 (block_size 대비)
    next_const_x = 1
    next_const_y = 8
    hold_const_x = 1
    hold_const_y = 3
    holdt_const_y = 1
    nextt_const_y = 6
    scoret_const_y = 12
    scorev_const_y = 13
    levelt_const_y = 15.5
    levelv_const_y = 16.5
    goalt_const_y = 18.5
    goalv_const_y = 19.5

    nmino_const_y = 8
    hmino_const_y = 3

    rot_help = 3


class button:  # 버튼객체
    def __init__(
        self,
        initial_width,
        initial_height,
        x_rate,
        y_rate,
        width_rate,
        height_rate,
        text,
    ):  # 버튼생성
        self.x = initial_width * x_rate  # 버튼 x좌표
        self.y = initial_height * y_rate  # 버튼 y좌표
        self.width = int(initial_width * width_rate)  # 버튼 너비
        self.height = int(initial_height * height_rate)  # 버튼 높이
        self.x_rate = x_rate  # initial_width * x_rate = x좌표
        self.y_rate = y_rate  # initial_height * y_rate = y좌표
        self.width_rate = width_rate  # initial_width * width_rate = 버튼 너비
        self.height_rate = height_rate  # initial_height * height_rate = 버튼 높이
        self.text = text  # 라벨

    def change(self, initial_width, initial_height):  # 버튼 위치, 크기 바꾸기
        self.x = initial_width * self.x_rate  # x좌표
        self.y = initial_height * self.y_rate  # y좌표
        self.width = int(initial_width * self.width_rate)  # 너비
        self.height = int(initial_height * self.height_rate)  # 높이

    def draw(self, win, outline=None):  # 버튼 보이게 만들기
        if outline:
            draw_text(screen, self.text, self.x, self.y, self.width, self.height)

    def isOver(self, pos):  # 마우스의 위치에 따라 버튼 누르기 pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (
                self.height / 2
            ):
                return True
        return False

    def isOver_2(self, pos):  # start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 8) and pos[1] < self.y + (
                self.height / 8
            ):  # 243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
                return True
        return False


# button
origianl_bnt = button(
    initial_width, initial_height, 0.32, 0.35, 0.2, 0.4, text1
)  # 순서 조금 꼬임
rotate_bnt = button(initial_width, initial_height, 0.32, 0.45, 0.2, 0.4, text3)
dual_bnt = button(initial_width, initial_height, 0.32, 0.55, 0.2, 0.4, text5)
blackout_bnt = button(initial_width, initial_height, 0.32, 0.65, 0.2, 0.4, text7)
info_bnt = button(initial_width, initial_height, 0.32, 0.75, 0.2, 0.4, text9)
goto_bnt = button(initial_width, initial_height, 0.4, 0.35, 0.2, 0.4, text13)
esc_bnt = button(initial_width, initial_height, 0.4, 0.35, 0.2, 0.4, pause_start)

bnt_list = [origianl_bnt, blackout_bnt, rotate_bnt, info_bnt, dual_bnt, goto_bnt, esc_bnt]

# Draw button text
def draw_text(window, text, x, y, width, height):
    x = x - (width / 2)
    window.blit(text, (x, y))


# with open("leaderboard.txt") as f:
#     lines = f.readlines()
# lines = [line.rstrip("\n") for line in open("leaderboard.txt")]
#
# leaders = {"AAA": 0, "BBB": 0, "CCC": 0}
# for i in lines:
#     leaders[i.split(" ")[0]] = int(i.split(" ")[1])
# leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
#
# matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
