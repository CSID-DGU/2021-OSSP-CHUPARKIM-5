# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
from mino import *
from random import *
from pygame.locals import *

# Define
block_size = 17 # Height, width of single block
width = 10 # Board width
height = 20 # Board height
framerate = 30 # Bigger -> Slower

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((750,600))
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")

class ui_variables:
    # Fonts
    font_path = "./assets/fonts/DungGeunMo.ttf" #일단 둥근모 폰트 테스트
    font_path_b = "./assets/fonts/DungGeunMo.ttf"
    font_path_i = "./assets/fonts/DungGeunMo.ttf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)  #카피라이트  - title_info랑 연결

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
    black = (10, 10, 10) #rgb(10, 10, 10)
    white = (255, 255, 255) #rgb(255, 255, 255)
    grey_1 = (26, 26, 26) #rgb(26, 26, 26)
    grey_2 = (35, 35, 35) #rgb(35, 35, 35)
    grey_3 = (55, 55, 55) #rgb(55, 55, 55)

    # Tetrimino colors
    cyan = (69, 206, 204) #rgb(69, 206, 204) # I
    blue = (64, 111, 249) #rgb(64, 111, 249) # J
    orange = (253, 189, 53) #rgb(253, 189, 53) # L
    yellow = (246, 227, 90) #rgb(246, 227, 90) # O
    green = (98, 190, 68) #rgb(98, 190, 68) # S
    pink = (242, 64, 235) #rgb(242, 64, 235) # T
    red = (225, 13, 27) #rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]

############### DualScreenMode 함수  #################
def draw_mino2(x,y,mino,r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom2(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix2[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix2[x + j][y + i] = grid[i][j]

def erase_mino2(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix2[i][j] == 8:
                matrix2[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix2[x + j][y + i] = 0

def is_bottom2(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix2[x + j][y + i + 1] != 0 and matrix2[x + j][y + i + 1] != 8:
                    return True
    return False

def is_stackable2(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix2[3 + j][i] != 0:
                return False
    return True

# Returns true if mino is at the left edge
def is_leftedge2(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix2[x + j - 1][y + i] != 0:
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge2(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix2[x + j + 1][y + i] != 0:
                    return True

    return False

# Returns true if turning right is possible
def is_turnable_r2(x, y, mino, r):
    if r != 3: #오른쪽으로 도니 r+1되는 mino가 그려질 수 있는지 check해야 되므로 3포함 안함
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else: # 4번째 형태의 mino를 한번 돌리면 다시 첫번째 형태가 됨
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix2[x + j][y + i] != 0:
                    return False

    return True


def draw_board2(next,hold,score,level,goal):

    # # Draw sidebar 흰색 사이드바 그림
    # pygame.draw.rect(
    #     screen,
    #     ui_variables.white,
    #     Rect(400, 100, 96, 374) #(x축,y축, 가로, 세로), 위치 재지정 해줄것


    # Draw next mino 다음 내려올 mino그림
    grid_n = tetrimino.mino_map[next - 1][0] # 다음 내려올 mino 정보 1

    for i in range(4):
        for j in range(4):
            dx = 600 + block_size * j #next mino그릴 좌표, 재지정 해줄 것
            dy = 300 + block_size * i #next mino그릴 좌표, 재지정 해줄 것
            if grid_n[i][j] != 10:  #이 부분 next minp가 계속 안겹치게 하기 위해서
                pygame.draw.rect(screen, ui_variables.grey_1, Rect(dx, dy, block_size, block_size))
            if grid_n[i][j] != 0: #하나씩 검사해서 그려 줌
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size,block_size)
                )
    # Draw hold mino - nextmino 그려주는거랑 똑같음
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 610 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )
    # Set max score
    if score > 999999:
        score = 999999

    # # Draw texts
    # text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    # text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    # text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    # score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    # text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    # level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    # text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    # goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    #
    # # Place texts
    # screen.blit(text_hold, (215, 14))  #텍스트를 생성해서 복사하고 이걸 해당 좌표에 붙여넣기
    # screen.blit(text_next, (215, 104))
    # screen.blit(text_score, (215, 194))
    # screen.blit(score_value, (220, 210))
    # screen.blit(text_level, (215, 254))
    # screen.blit(level_value, (220, 270))
    # screen.blit(text_goal, (215, 314))
    # screen.blit(goal_value, (220, 330))

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):
            dx =  17 + block_size * x
            dy =  17 + block_size * y
            draw_block(dx+400, dy+100, ui_variables.t_color[matrix2[x][y + 1]])



###################################################

# Draw block 격자무늬 그림
def draw_block(x, y, color): #이게 뭘 그리는지 모르겠음, color 바꾸면 회색격자 바뀌기는 하는데, 내려오는 block이 안보임
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(  #회색격자 감싸는 검정색 격자
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

# Draw game screen
def draw_board1(next, hold, score, level, goal):
    # screen.fill(ui_variables.grey_1) # 게임배경을 검정으로 해서 스타트 화면 가림

    # Draw sidebar 흰색 사이드바 그림
    # pygame.draw.rect(
    #     screen,
    #     ui_variables.white,
    #     Rect(204, 0, 96, 374) #(x축,y축, 가로, 세로) # 보드 위치를 직접적으로 지정해줬
    # )

    # Draw next mino 다음 내려올 mino그림
    grid_n = tetrimino.mino_map[next - 1][0] # 다음 내려올 미노에 대한 정보

    for i in range(4):
        for j in range(4):
            dx = 300 + block_size * j #next mino그릴 좌표 설정
            dy = 300 + block_size * i
            if grid_n[i][j] != 10:  #이 부분 next minp가 계속 안겹치게 하기 위해서  꼭 참조
                pygame.draw.rect(screen, ui_variables.grey_1, Rect(dx, dy, block_size, block_size))
            if grid_n[i][j] != 0: #하나씩 검사해서 그려 줌
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino - nextmino 그려주는거랑 똑같음
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 350 + block_size * j
                dy = 350 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    # text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    # text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    # text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    # score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    # text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    # level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    # text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    # goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)
    #
    # # Place texts
    # screen.blit(text_hold, (215, 14))  #텍스트를 생성해서 복사하고 이걸 해당 좌표에 붙여넣기
    # screen.blit(text_next, (215, 104))
    # screen.blit(text_score, (215, 194))
    # screen.blit(score_value, (220, 210))
    # screen.blit(text_level, (215, 254))
    # screen.blit(level_value, (220, 270))
    # screen.blit(text_goal, (215, 314))
    # screen.blit(goal_value, (220, 330))

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):
            # dx = 17 + block_size * (width-x) #180도
            # dy = 17 + block_size * (height-y)

            # dx = 17 + block_size * (height-y) # 270
            # dy = 17 + block_size * x

            # dx = 17 + block_size * y # 90
            # dy = 17 + block_size * (width-x)

            dx = 17  + block_size * x   #17은 그려지는 위치값의 가중치.
            dy = 17 + block_size * y

            draw_block(dx+100, dy+100, ui_variables.t_color[matrix[x][y + 1]])

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r): #바닥인지 아닌지 검색 해서 일때까지  y좌표값 증가해서 바닥 찾기
        ty += 1

    # Draw ghost - 그림자 생성하기
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i +1] != 0 and matrix[x + j][y + i +1] != 8:
                    return True

    return False

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3: #오른쪽으로 도니 r+1되는 mino가 그려질 수 있는지 check해야 되므로 3포함 안함
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else: # 4번째 형태의 mino를 한번 돌리면 다시 첫번째 형태가 됨
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False
    return True

def PauseScreen():
    global pause
    global blink
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 300) #(eventnumber, interval-밀리세컨)
            draw_board1(next_mino, hold_mino, score, level, goal)

            pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.white)
            pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.white)

            screen.blit(pause_text, (43, 100))
            if blink:
                screen.blit(pause_start, (40, 160))
                blink = False
            else:
                blink = True
            pygame.display.update()
        elif event.type == KEYDOWN:
            erase_mino(dx, dy, mino, rotation)
            if event.key == K_ESCAPE:
                pause = False
                ui_variables.click_sound.play()
                pygame.time.set_timer(pygame.USEREVENT, 1)
                print("pause out:", pause)
    return

# Initial values
blink = False
start = False
pause = False
done = False
game_over = False

score = 0
level = 1
goal = level * 5
bottom_count = 0
hard_drop = False

dx, dy = 3, 0 # Minos location status - 처음미노가 떨어질 현재 좌표의 초기화
rotation = 0 # Minos rotation status

mino = randint(1, 7) # Current mino
next_mino = randint(1, 7) # Next mino

hold = False # Hold status
hold_mino = -1 # Holded mino

name_location = 0
name = [65, 65, 65] # 65 = A

with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)] # Board matrix 보드에 대한 정보

#####initial value add #########
dx2, dy2 = 3,0
rotation2 = 0

score2 = 0
level2 = 1
goal2 = level2 * 5
hard_drop2 = False
bottom_count2 = 0

mino2 = randint(1, 7)  # Next mino1
next_mino2 = randint(1, 7)

hold2 = False
hold_mino2 = -1

matrix2 = [[0 for y in range(height + 1)] for x in range(width)]

board_state = True #True 일때 board 1, False일때 board 2


###########################################################
# Loop Start
###########################################################


while not done:
    # Pause screen
    if pause:
        PauseScreen()
    # Game screen
    elif start:
        # StartScreen()
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 10 )
                    # keys_pressed = pygame.key.get_pressed()  #임시로 막아 놓음.
                    # if keys_pressed[K_DOWN]:
                    #     pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    # else:
                    #     pygame.time.set_timer(pygame.USEREVENT, framerate * 10)


                # Draw a mino
                draw_mino(dx,dy, mino, rotation)
                draw_mino2(dx2,dy2, mino2, rotation2)
                ##board 두개 그리
                #draw_multiboard(next_mino, hold_mino, score, level ,goal, next_mino2, hold_mino2)
                draw_board1(next_mino, hold_mino, score, level, goal)
                draw_board2(next_mino2, hold_mino2, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx,dy,mino, rotation)
                    erase_mino2(dx2,dy2,mino2, rotation2)
                # Move mino down  +  Create new mino
                #보드 1
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1 #파이게임 좌표는 왼쪽 상단에서 0,0
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        #draw_mino2(dx2, dy2, mino2, rotation2)
                        #draw_multiboard(next_mino, hold_mino, score, level ,goal, next_mino2, hold_mino2)
                        draw_board1(next_mino, hold_mino, score, level, goal)
                        #draw_board2(next_mino2, hold_mino2, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            # print("gameover= ", game_over)

                            game_over = True
                            # print(game_over)
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                #보드 2
                if not is_bottom2(dx2, dy2, mino2, rotation2):
                    dy2 += 1 #파이게임 좌표는 왼쪽 상단에서 0,0
                else:
                    if hard_drop2 or bottom_count2 == 6:
                        hard_drop2 = False
                        bottom_count2 = 0
                        score2 += 10 * level
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

                        if is_stackable2(next_mino2):
                            mino2 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx2, dy2 = 3, 0
                            rotation2 = 0
                            hold2 = False
                        else:
                            start = False
                            # print(game_over2)
                            # print(matrix2)
                            game_over = True
                            # print("2",game_over)
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count2 += 1

                # Erase line
                erase_count = 0
                erase_count2 = 0
                ##board1
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0 or matrix[i][j] == 8:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5

                #board2
                for j in range(21):
                    is_full2 = True
                    for i in range(10):
                        if matrix2[i][j] == 0:
                            is_full2 = False
                    if is_full2:
                        erase_count2 += 1
                        k2 = j
                        while k2 > 0:
                            for i in range(10):
                                matrix2[i][k2] = matrix2[i][k2 - 1]
                            k2 -= 1

                if erase_count2 == 1:
                    ui_variables.single_sound.play()
                    score2 += 50 * level2
                elif erase_count2 == 2:
                    ui_variables.double_sound.play()
                    score2 += 150 * level2
                elif erase_count2 == 3:
                    ui_variables.triple_sound.play()
                    score2 += 350 * level2
                elif erase_count2 == 4:
                    ui_variables.tetris_sound.play()
                    score2 += 1000 * level2
                    goal2 -= erase_count2
                if goal2 < 1 and level2 < 15:
                    level2 += 1
                    goal2 += level2 * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx,dy,mino, rotation)
                erase_mino2(dx2,dy2,mino2, rotation2)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                elif event.key == K_q:  #board_state로 플레히는 board 전호나
                    board_state = not board_state #반전시키는 부분
                    print(board_state)
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    if (board_state==True):
                        while not is_bottom(dx, dy, mino, rotation):
                            dy += 1
                        hard_drop = True
                        draw_mino(dx, dy, mino, rotation)
                        draw_board1(next_mino, hold_mino, score, level, goal)
                    else:
                        while not is_bottom2(dx2, dy2, mino2, rotation2):
                            dy2 += 1
                        hard_drop2 = True
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if(board_state == True):
                        if hold == False:
                            ui_variables.move_sound.play()
                            if hold_mino == -1:
                                hold_mino = mino
                                mino = next_mino
                                next_mino = randint(1, 7)
                            else:
                                hold_mino, mino = mino, hold_mino
                            dx, dy = 3, 0
                            rotation = 0
                            hold = True
                        draw_mino(dx, dy, mino, rotation)
                        draw_board1(next_mino, hold_mino, score, level, goal)
                    else:
                        if hold2 == False:
                            ui_variables.move_sound.play()
                            if hold_mino2 == -1:
                                hold_mino2 = mino2
                                mino2 = next_mino2
                                next_mino2 = randint(1, 7)
                            else:
                                hold_mino2, mino2 = mino2, hold_mino2

                            dx2, dy2 = 3, 0
                            rotation2 = 0
                            hold2 = True
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

                # Turn right
                elif event.key == K_x:
                    if(board_state == True):
                        if is_turnable_r(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            rotation += 1
                        # Kick
                        elif is_turnable_r(dx, dy - 1, mino, rotation):
                            ui_variables.move_sound.play()
                            dy -= 1
                            rotation += 1
                        elif is_turnable_r(dx + 1, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                            rotation += 1
                        elif is_turnable_r(dx - 1, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                            rotation += 1
                        elif is_turnable_r(dx, dy - 2, mino, rotation):
                            ui_variables.move_sound.play()
                            dy -= 2
                            rotation += 1
                        elif is_turnable_r(dx + 2, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 2
                            rotation += 1
                        elif is_turnable_r(dx - 2, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 2
                            rotation += 1
                        if rotation == 4:
                            rotation = 0
                        draw_mino(dx, dy, mino, rotation)
                        draw_board1(next_mino, hold_mino, score, level, goal)

                    else:
                        if is_turnable_r2(dx2, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            rotation2 += 1
                        # Kick
                        elif is_turnable_r2(dx2, dy2 - 1, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dy2 -= 1
                            rotation2 += 1
                        elif is_turnable_r2(dx2 + 1, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 += 1
                            rotation2 += 1
                        elif is_turnable_r2(dx2 - 1, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 -= 1
                            rotation2 += 1
                        elif is_turnable_r2(dx2, dy2 - 2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dy2 -= 2
                            rotation2 += 1
                        elif is_turnable_r2(dx2 + 2, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 += 2
                            rotation2 += 1
                        elif is_turnable_r2(dx2 - 2, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 -= 2
                            rotation2 += 1
                        if rotation2 == 4:
                            rotation2 = 0
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

                # Move left
                elif event.key == K_LEFT:
                    if(board_state == True):
                        if not is_leftedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx -= 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_board1(next_mino, hold_mino, score, level, goal)
                    else:
                        if not is_leftedge2(dx2, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 -= 1
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

                # Move right
                elif event.key == K_RIGHT:
                    if(board_state == True):
                        if not is_rightedge(dx, dy, mino, rotation):
                            ui_variables.move_sound.play()
                            dx += 1
                        draw_mino(dx, dy, mino, rotation)
                        draw_board1(next_mino, hold_mino, score, level, goal)
                    else:
                        if not is_rightedge2(dx2, dy2, mino2, rotation2):
                            ui_variables.move_sound.play()
                            dx2 += 1
                        draw_mino2(dx2, dy2, mino2, rotation2)
                        draw_board2(next_mino2, hold_mino2, score, level, goal)

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render("Press return to continue", 1, ui_variables.white)

                #draw_multiboard(next_mino, hold_mino, score, level ,goal, next_mino2, hold_mino2)
                draw_board1(next_mino, hold_mino, score, level, goal)
                draw_board2(next_mino2, hold_mino2, score, level, goal)

                screen.blit(over_text_1, (58, 75))
                screen.blit(over_text_2, (62, 105))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                screen.blit(name_1, (65, 147))
                screen.blit(name_2, (95, 147))
                screen.blit(name_3, (125, 147))

                if blink:
                    screen.blit(over_start, (32, 195))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (65, 145))
                    elif name_location == 1:
                        screen.blit(underbar_2, (95, 145))
                    elif name_location == 2:
                        screen.blit(underbar_3, (125, 145))
                    blink = True

                pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)] # height
                    ##### board2 초기화
                    dx2, dy2 = 3,0
                    rotation2 = 0

                    score2 = 0
                    level2 = 1
                    goal2 = level2 * 5
                    hard_drop2 = False
                    bottom_count2 = 0

                    mino2 = randint(1, 7)  # Next mino1
                    next_mino2 = randint(1, 7)

                    hold2 = False
                    hold_mino2 = -1

                    matrix2 = [[0 for y in range(height + 1)] for x in range(width)]

                    board_state = True #True 일때 board 1, False일때 board 2
                    #####

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # Start screen
    else:

        # pygame.time.set_timer(pygame.USEREVENT, 300)
        screen.fill(ui_variables.white)
        pygame.draw.rect(
            screen,
            ui_variables.grey_1,
            Rect(0, 187, 300, 187)
        )

        title = ui_variables.h1.render("PYTRIS™", 1, ui_variables.grey_1)
        title_start = ui_variables.h5.render("Press space to start", 1, ui_variables.white)
        title_info = ui_variables.h6.render("Copyright (c) 2017 Jason Kim All Rights Reserved.", 1, ui_variables.white)

        leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)

        if blink:
            screen.blit(title_start, (92, 195))
            blink = False
        else:
            blink = True

        screen.blit(title, (65, 120))
        screen.blit(title_info, (40, 335))

        screen.blit(leader_1, (10, 10))
        screen.blit(leader_2, (10, 23))
        screen.blit(leader_3, (10, 36))

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    start = True
                    screen.fill(ui_variables.grey_1)
        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
