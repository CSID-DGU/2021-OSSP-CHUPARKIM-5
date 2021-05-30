# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
from mino import *
from random import *
from pygame.locals import *

# Define
block_size = 17  # Height, width of single block
width = 10  # Board width
height = 20  # Board height
framerate = 30  # Bigger -> Slower

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((750, 600))
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")

locx=0 # for move left, right
locy=0 # for move up, down

class ui_variables:
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

    # Background colors for blackoutmode !(Modification required)
    black = (10, 10, 10)  # rgb(10, 10, 10)
    white = (10, 10, 10)  # rgb(255, 255, 255)
    grey_1 = (10, 10, 10)  # rgb(26, 26, 26)
    grey_2 = (10, 10, 10)  # rgb(35, 35, 35)
    grey_3 = (10, 10, 10)  # rgb(55, 55, 55)

    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]


def blackout_mode():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause
    global locy, locx
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            # Set speed
            if not game_over:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[K_DOWN]:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                else:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

            # Draw a mino
            draw_mino(dx, dy, mino, rotation)
            draw_board_b(next_mino, hold_mino, score, level, goal)

            # Erase a mino
            if not game_over:
                erase_mino(dx, dy, mino, rotation)

            # Move mino down
            if not is_bottom(dx, dy, mino, rotation):
                dy += 1
                locy -= 17

            # Create new mino
            else:
                if hard_drop or bottom_count == 6:
                    hard_drop = False
                    bottom_count = 0
                    score += 10 * level
                    locy = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board_b(next_mino, hold_mino, score, level, goal)
                    if is_stackable(next_mino):
                        mino = next_mino
                        next_mino = randint(1, 7)
                        dx, dy = 3, 0
                        rotation = 0
                        hold = False
                    else:
                        start = False
                        game_over = True
                        pygame.time.set_timer(pygame.USEREVENT, 1)
                else:
                    bottom_count += 1

            # Erase line
            erase_count = 0
            for j in range(21):
                is_full = True
                for i in range(10):
                    if matrix[i][j] == 0:
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

            # Increase level
            goal -= erase_count
            if goal < 1 and level < 15:
                level += 1
                goal += level * 5
                framerate = int(framerate * 0.8)

        elif event.type == KEYDOWN:
            erase_mino(dx, dy, mino, rotation)
            if event.key == K_ESCAPE:
                ui_variables.click_sound.play()
                pause = True
            # Hard drop
            elif event.key == K_SPACE:
                ui_variables.drop_sound.play()
                while not is_bottom(dx, dy, mino, rotation):
                    dy += 1
                    locy -= 17
                    locx=0
                hard_drop = True
                pygame.time.set_timer(pygame.USEREVENT, 1)
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Hold
            elif event.key == K_LSHIFT or event.key == K_c:
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
                    locx = 0
                    locy = 0
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Turn right
            elif event.key == K_UP or event.key == K_x:
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
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Turn left
            elif event.key == K_z or event.key == K_LCTRL:
                if is_turnable_l(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    rotation -= 1
                # Kick
                elif is_turnable_l(dx, dy - 1, mino, rotation):
                    ui_variables.move_sound.play()
                    dy -= 1
                    rotation -= 1
                elif is_turnable_l(dx + 1, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                    rotation -= 1
                elif is_turnable_l(dx - 1, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                    rotation -= 1
                elif is_turnable_l(dx, dy - 2, mino, rotation):
                    ui_variables.move_sound.play()
                    dy -= 2
                    rotation += 1
                elif is_turnable_l(dx + 2, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 2
                    rotation += 1
                elif is_turnable_l(dx - 2, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 2
                if rotation == -1:
                    rotation = 3
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Move left
            elif event.key == K_LEFT:
                if not is_leftedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                    locx += 17
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Move right
            elif event.key == K_RIGHT:
                if not is_rightedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                    locx -= 17
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)

    pygame.display.update()
# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, Rect(x, y, block_size, block_size))
    pygame.draw.rect(screen, ui_variables.grey_1, Rect(x, y, block_size, block_size), 1)


# Draw blackout-mode game screen
def draw_board_b(next, hold, score, level, goal):
    screen.fill(ui_variables.black)

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + 188 + block_size * j
                dy = 50 + 113 + block_size * i
                if grid_h[i][j] != 0:
                    # pygame.draw.rect(
                    #     screen,
                    #     ui_variables.t_color[grid_h[i][j]],
                    #     Rect(dx, dy, block_size, block_size),
                    # )
                    pass

    # Set max score
    if score > 999999:
        score = 999999

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 17 + 188 + 80 + block_size * x + locx
            dy = 17 + 113 + 100 + block_size * y + locy
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
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
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
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
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True


# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

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
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True


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

###########################################################
# Loop Start
###########################################################

while not done:
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                draw_board_b(next_mino, hold_mino, score, level, goal)

                pause_text = ui_variables.h2.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.h5.render(
                    "Press esc to continue", 1, ui_variables.white
                )

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

    # Game screen
    elif start:
        blackout_mode()
    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render(
                    "Press return to continue", 1, ui_variables.white
                )

                draw_board_b(next_mino, hold_mino, score, level, goal)
                screen.blit(over_text_1, (58, 75))
                screen.blit(over_text_2, (62, 105))

                name_1 = ui_variables.h2.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2.render(chr(name[2]), 1, ui_variables.white)

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

                    outfile = open("leaderboard.txt", "a")
                    outfile.write(
                        chr(name[0])
                        + chr(name[1])
                        + chr(name[2])
                        + " "
                        + str(score)
                        + "\n"
                    )
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
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open("leaderboard.txt") as f:
                        lines = f.readlines()
                    lines = [line.rstrip("\n") for line in open("leaderboard.txt")]

                    leaders = {"AAA": 0, "BBB": 0, "CCC": 0}
                    for i in lines:
                        leaders[i.split(" ")[0]] = int(i.split(" ")[1])
                    leaders = sorted(
                        leaders.items(), key=operator.itemgetter(1), reverse=True
                    )

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
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    start = True

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
