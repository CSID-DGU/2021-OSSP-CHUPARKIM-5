import pygame
import operator
from mino import *
from random import *
from pygame.locals import *
from game_var import *

pygame.init()

#######################################################
# ------------------모든 게임 공통 함수들------------------#
#######################################################

# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, Rect(x, y, block_size, block_size))
    pygame.draw.rect(screen, ui_variables.black, Rect(x, y, block_size, block_size), 1)


# Draw game screen
def draw_board(next, hold, score, level, goal):
    screen.fill(ui_variables.black)

    # Draw sidebar
    pygame.draw.rect(screen, ui_variables.white, Rect(w_1 + w_2, h_2, w_3, temp))

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 220 + w_2 + block_size * j
            dy = 140 + h_2 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + w_2 + block_size * j
                dy = 50 + h_2 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size),
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (215 + w_2, 14 + h_2))
    screen.blit(text_next, (215 + w_2, 104 + h_2))
    screen.blit(text_score, (215 + w_2, 194 + h_2))
    screen.blit(score_value, (220 + w_2, 210 + h_2))
    screen.blit(text_level, (215 + w_2, 254 + h_2))
    screen.blit(level_value, (220 + w_2, 270 + h_2))
    screen.blit(text_goal, (215 + w_2, 314 + h_2))
    screen.blit(goal_value, (220 + w_2, 330 + h_2))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = w_2 + block_size * (x + 1)
            dy = h_2 + block_size * (y + 1)
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


# Draw blackout-mode game screen
def draw_board_b(next, hold, score, level, goal, locx, locy):

    screen.fill(ui_variables.black)

    # Set max score
    if score > 999999:
        score = 999999

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 17 + 290 + block_size * x + locx
            dy = 17 + 170 + block_size * y + locy
            draw_block(dx, dy, ui_variables.t_color_b[matrix[x][y + 1]])


def draw_board_r(next, hold, score, level, goal,num_of_disrot):
    screen.fill(ui_variables.black)

    # Draw sidebar
    if num_of_disrot == 0:  # 0회전
        pygame.draw.rect(
            screen, ui_variables.white, Rect(204 + 188, 0 + 113, 96 + 74, 374)
        )
    elif num_of_disrot == 1:  # 1회전
        pygame.draw.rect(
            screen, ui_variables.white, Rect(0 + 188, 0 + 113 + 204, 374, 96 + 74)
        )
    elif num_of_disrot == 2:  # 2회전
        pygame.draw.rect(
            screen, ui_variables.white, Rect(0 + 188, 0 + 113, 96 + 74, 374)
        )
    elif num_of_disrot == 3:  # 3회전
        pygame.draw.rect(
            screen, ui_variables.white, Rect(0 + 188, 0 + 113, 374, 96 + 74)
        )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 220 + 188 + block_size * j
            dy = 140 + 113 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + 188 + block_size * j
                dy = 50 + 113 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size),
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    deg = 0  # 0회전 = 0
    # deg = 270  # 1회전 =270도
    # deg = 180 #2회전 = 180도
    # deg = 90 #3회전 = 90도
    text_hold = pygame.transform.rotate(
        ui_variables.h5.render("HOLD", 1, ui_variables.black), deg
    )
    text_next = pygame.transform.rotate(
        ui_variables.h5.render("NEXT", 1, ui_variables.black), deg
    )
    text_score = pygame.transform.rotate(
        ui_variables.h5.render("SCORE", 1, ui_variables.black), deg
    )
    score_value = pygame.transform.rotate(
        ui_variables.h4.render(str(score), 1, ui_variables.black), deg
    )
    text_level = pygame.transform.rotate(
        ui_variables.h5.render("LEVEL", 1, ui_variables.black), deg
    )
    level_value = pygame.transform.rotate(
        ui_variables.h4.render(str(level), 1, ui_variables.black), deg
    )
    text_goal = pygame.transform.rotate(
        ui_variables.h5.render("GOAL", 1, ui_variables.black), deg
    )
    goal_value = pygame.transform.rotate(
        ui_variables.h4.render(str(goal), 1, ui_variables.black), deg
    )

    # Place texts
    screen.blit(text_hold, (215 + 188, 14 + 113))
    screen.blit(text_next, (215 + 188, 104 + 113))
    screen.blit(text_score, (215 + 188, 194 + 113))
    screen.blit(score_value, (220 + 188, 210 + 113))
    screen.blit(text_level, (215 + 188, 254 + 113))
    screen.blit(level_value, (220 + 188, 270 + 113))
    screen.blit(text_goal, (215 + 188, 314 + 113))
    screen.blit(goal_value, (220 + 188, 330 + 113))

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):
            if num_of_disrot == 0:  # 0회전
                dx = 17 + 188 + block_size * x
                dy = 17 + 113 + block_size * y
            elif num_of_disrot == 1:  # 1회전 = 270도 회전
                dx = 17 + 188 + block_size * (height - y - 1)
                dy = 17 + 113 + block_size * x
            elif num_of_disrot == 2:  # 2회전 = 180도 회전
                dx = 17 + 188 + 170 + block_size * (width - x)
                dy = 17 + 113 + block_size * (height - y - 1)
            elif num_of_disrot == 3:  # 3회전 = 90도 회전
                dx = 17 + 188 + block_size * y
                dy = 17 + 113 + 170 + block_size * (width - x - 1)

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


# 크기 조정 함수
def update_display():
    w, h = pygame.display.get_surface().get_size()
    current_rate = h / w
    global block_size, temp, w_1, w_2, w_3, h_2
    if h / w >= 0.8:
        block_size = round(17 * w / 750)
    else:
        block_size = round(17 * h / 600)
    temp = block_size * 22  # 374가 바뀔 부분
    w_1 = block_size * 12  # 204가 바뀔 부분
    w_2 = (w - temp) / 2  # 188이 바뀔 부분
    w_3 = block_size * 10  # 96 + 74가 바뀔 부분
    h_2 = (h - temp) / 2  # 113이 바뀔 부분
