import pygame
import operator
from mino import *
from random import *
from pygame.locals import *

# from game_func import *
from game_var import *


#######################################공통함수##########################
# Draw block
def draw_block_b(x, y, color):
    pygame.draw.rect(screen, color, Rect(x, y, block_size, block_size))
    pygame.draw.rect(screen, ui_variables.black, Rect(x, y, block_size, block_size), 1)


def draw_block(x, y, color):
    pygame.draw.rect(screen, color, Rect(x, y, block_size, block_size))
    pygame.draw.rect(screen, ui_variables.grey_1, Rect(x, y, block_size, block_size), 1)


# Draw blackout-mode game screen
def draw_board_b(next, hold, score, level, goal):

    screen.fill(ui_variables.black)

    # Set max score
    if score > 999999:
        score = 999999

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = w_2 + w_3 / 2 + block_size * x + locx
            dy = h_1 + temp / 2 + block_size * y + locy
            draw_block_b(dx, dy, ui_variables.t_color_b[matrix[x][y + 1]])


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


def draw_board(next, hold, score, level, goal):
    screen.fill(ui_variables.black)
    screen.blit(background, (0, 0))
    screen.blit(logo, (block_size + w_1 + w_2, block_size * game_loc.holdt_const_y))
    pygame.draw.line(screen, ui_variables.red_b, [w_2, h_1], [w_2 + temp, h_1], 5)
    pygame.draw.line(screen, ui_variables.red_b, [w_2, h_1], [w_2, h_1 + temp], 5)
    pygame.draw.line(
        screen, ui_variables.red_b, [w_2 + temp, h_1], [w_2 + temp, h_1 + temp], 5
    )
    pygame.draw.line(
        screen, ui_variables.red_b, [w_2, h_1 + temp], [w_2 + temp, h_1 + temp], 5
    )

    # Draw sidebar
    # pygame.draw.rect(screen, ui_variables.black, Rect(w_1 + w_2, h_1, w_3, temp))

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = block_size * game_loc.next_const_x + w_1 + w_2 + block_size * j
            dy = block_size * game_loc.next_const_y + h_1 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold != -1:
        for i in range(4):
            for j in range(4):
                dx = block_size * game_loc.hold_const_x + w_1 + w_2 + block_size * j
                dy = block_size * game_loc.hold_const_y + h_1 + block_size * i
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
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.white)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.white)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.white)

    # Place texts
    screen.blit(
        text_hold, (block_size + w_1 + w_2, block_size * game_loc.holdt_const_y + h_1)
    )
    screen.blit(
        text_next, (block_size + w_1 + w_2, block_size * game_loc.nextt_const_y + h_1)
    )
    screen.blit(
        text_score, (block_size + w_1 + w_2, block_size * game_loc.scoret_const_y + h_1)
    )
    screen.blit(
        score_value,
        (block_size + w_1 + w_2, block_size * game_loc.scorev_const_y + h_1),
    )
    screen.blit(
        text_level, (block_size + w_1 + w_2, block_size * game_loc.levelt_const_y + h_1)
    )
    screen.blit(
        level_value,
        (block_size + w_1 + w_2, block_size * game_loc.levelv_const_y + h_1),
    )
    screen.blit(
        text_goal, (block_size + w_1 + w_2, block_size * game_loc.goalt_const_y + h_1)
    )
    screen.blit(
        goal_value, (block_size + w_1 + w_2, block_size * game_loc.goalv_const_y + h_1)
    )

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = w_2 + block_size * (x + 1)
            dy = h_1 + block_size * (y + 1)
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


#####################################################################


############### 모드추가 함수  ################################
def draw_mino2(x, y, mino, r):
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
    if r != 3:  # 오른쪽으로 도니 r+1되는 mino가 그려질 수 있는지 check해야 되므로 3포함 안함
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:  # 4번째 형태의 mino를 한번 돌리면 다시 첫번째 형태가 됨
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix2[x + j][y + i] != 0:
                    return False

    return True


def draw_board2(next, hold, score, level, goal):
    # Set max score
    if score > 999999:
        score = 999999

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):
            dx = block_size +w_b2+ block_size * x
            dy = block_size + h_1 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix2[x][y + 1]])
            # draw_block(dx + 300, dy + 100, ui_variables.t_color[matrix2[x][y + 1]])


def draw_board1(next, hold, score, level, goal):
    # Set max score
    if score > 999999:
        score = 999999

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):

            dx = block_size + w_b1 + block_size * x
            dy = block_size + h_1 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])
            # draw_block(dx + 100, dy + 100, ui_variables.t_color[matrix[x][y + 1]])


def update_display():
    global block_size, temp, w_1, w_2, w_3, h_1, background, w, h, pau, goto_bnt, esc_bnt, w_4,w_b1, w_b2, w_s, rank_w
    w, h = pygame.display.get_surface().get_size()
    current_rate = h / w
    if w < minimum_width:
        w = minimum_width
        pygame.display.set_mode((w, h), RESIZABLE)
    if h < minimum_height:
        h = minimum_height
        pygame.display.set_mode((w, h), RESIZABLE)
    if h / w >= 0.8:
        block_size = round(17 * w / 750)
    else:
        block_size = round(17 * h / 600)

    background = pygame.transform.scale(background, (w, h))
    pau = pygame.transform.scale(pau, (w, h))

    goto_bnt = button(w, h, 0.4, 0.35, 0.2, 0.4, text13)
    esc_bnt = button(w, 1.5 * h, 0.4, 0.35, 0.2, 0.4, pause_start)

    pos = pygame.mouse.get_pos()
    if pause == True:
        if goto_bnt.isOver_2(pos):
            goto_bnt.text = text14
        else:
            goto_bnt.text = text13

    temp = block_size * 22  # 374가 바뀔 부분
    w_1 = block_size * 12  # 204가 바뀔 부분
    w_2 = (w - temp) / 2  # 188이 바뀔 부분
    w_3 = block_size * 10  # 96 + 74가 바뀔 부분
    h_1 = (h - temp) / 2  # 113이 바뀔 부분

    w_d1_2 = (w - temp) / 5
    w_d2_2 = (w - temp) / 1.3
    rank_w = (
        w
        - 3 * game_loc.rank_mode_blank * block_size
        - game_loc.rank_info_blank * block_size
    ) / 2
    
    w_4 = (w - w_1 *3) /2 #w_2의 자리
    w_b1 = w_4 #보드 1의 x좌표
    w_b2 = w_4 + w_1 #보드 2의 x좌표
    w_s = w_4 + w_1 * 2 #사이드 바 x 좌
    d_draw_const = 0.9

def draw_dual_sidebar(block_size, next, hold, next2, hold2):
    pygame.draw.line(screen, ui_variables.red_b, [w_4, h_1], [w_4 + w_1 * 3, h_1], 5)
    pygame.draw.line(screen, ui_variables.red_b, [w_4, h_1], [w_4, h_1 + temp], 5)
    pygame.draw.line(screen, ui_variables.red_b, [w_4 + w_1 * 3, h_1], [w_4 +w_1 *3, h_1 + temp], 5)
    pygame.draw.line(screen, ui_variables.red_b, [w_4, h_1 + temp], [w_4 + w_1 * 3, h_1 + temp], 5)
    # 보드 1
    grid_n = tetrimino.mino_map[next - 1][0]  # 다음 내려올 미노에 대한 정보

    for i in range(4):
        for j in range(4):
            dx = block_size + w_s + block_size * j # next mino그릴 좌표 설정
            dy = block_size * game_loc.nmino_const_y + h_1 + block_size * i
            if grid_n[i][j] != 10:  # 이 부분 next minp가 계속 안겹치게 하기 위해서  꼭 참조
                pygame.draw.rect(
                    screen, ui_variables.black, Rect(dx, dy, block_size, block_size)
                )
            if grid_n[i][j] != 0:  # 하나씩 검사해서 그려 줌
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )

    # Draw hold mino - nextmino 그려주는거랑 똑같음
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = block_size + w_s + block_size * j
                dy = block_size * game_loc.hmino_const_y + h_1 + block_size * i
                if grid_n[i][j] != 10:  # 이 부분 next minp가 계속 안겹치게 하기 위해서  꼭 참조
                    pygame.draw.rect(
                        screen, ui_variables.black, Rect(dx, dy, block_size, block_size)
                    )
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size),
                    )
    # 보드 2
    grid_n = tetrimino.mino_map[next2 - 1][0]  # 다음 내려올 mino 정보 1

    for i in range(4):
        for j in range(4):
            dx = block_size + w_s * game_loc.nh_b2_const_x + block_size * j   # next mino그릴 좌표, 재지정 해줄 것
            dy = block_size * game_loc.nmino_const_y + h_1 + block_size * i  # next mino그릴 좌표, 재지정 해줄 것
            if grid_n[i][j] != 10:  # 이 부분 next minp가 계속 안겹치게 하기 위해서
                pygame.draw.rect(
                    screen, ui_variables.black, Rect(dx, dy, block_size, block_size)
                )
            if grid_n[i][j] != 0:  # 하나씩 검사해서 그려 줌
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )
    # Draw hold mino - nextmino 그려주는거랑 똑같음
    grid_h = tetrimino.mino_map[hold2 - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = block_size + w_s * game_loc.nh_b2_const_x + block_size * j
                dy = block_size * game_loc.hmino_const_y + h_1 + block_size * i
                if grid_n[i][j] != 10:  # 이 부분 next minp가 계속 안겹치게 하기 위해서  꼭 참조
                    pygame.draw.rect(
                        screen, ui_variables.black, Rect(dx, dy, block_size, block_size)
                    )
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size),
                    )
    pygame.draw.rect(screen,ui_variables.black,Rect(block_size + w_s,block_size * game_loc.scorev_const_y + h_1,block_size * 2, block_size *2)) #스코어 중첩방지를 위해 덮어 씌워기
    text_d1_hold = ui_variables.h5.render("HOLD_1", 1, ui_variables.white)
    text_d1_next = ui_variables.h5.render("NEXT_1", 1, ui_variables.white)
    text_d2_hold = ui_variables.h5.render("HOLD_2", 1, ui_variables.white)
    text_d2_next = ui_variables.h5.render("NEXT_2", 1, ui_variables.white)
    text_d_score = ui_variables.h5.render("SCORE", 1, ui_variables.white)
    text_d_level = ui_variables.h5.render("LEVEL", 1, ui_variables.white)
    text_d_goal = ui_variables.h5.render("GOAL", 1, ui_variables.white)
    d_score_value = ui_variables.h4.render(str(score+score2), 1, ui_variables.white)
    d_level_value =ui_variables.h4.render(str(level), 1, ui_variables.white)
    d_goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.white)
    screen.blit(
            text_d1_hold,
            (block_size + w_s, block_size * game_loc.holdt_const_y + h_1),
        )
    screen.blit(
            text_d1_next,
            (block_size + w_s, block_size * game_loc.nextt_const_y + h_1),
        )
    screen.blit(
            text_d2_hold,
            (block_size + w_s*game_loc.nh_b2_const_x, block_size * game_loc.holdt_const_y + h_1),
        )
    screen.blit(
            text_d2_next,
            (block_size + w_s*game_loc.nh_b2_const_x, block_size * game_loc.nextt_const_y + h_1),
        )
    screen.blit(
            text_d_score,
            (block_size + w_s, block_size * game_loc.scoret_const_y + h_1),
        )
    screen.blit(
            text_d_level,
            (block_size + w_s, block_size * game_loc.levelt_const_y + h_1),
        )
    screen.blit(
            text_d_goal,
            (block_size + w_s, block_size * game_loc.goalt_const_y + h_1),
        )
    screen.blit(
            d_score_value,
            (block_size + w_s, block_size * game_loc.scorev_const_y + h_1),
        )
    screen.blit(
            d_level_value,
            (block_size + w_s, block_size * game_loc.levelv_const_y + h_1),
        )
    screen.blit(
            d_goal_value,
            (block_size + w_s, block_size * game_loc.goalv_const_y + h_1),
        )

# ----------------------------------rotate ------------------------------------#
def draw_board_r(next, hold, score, level, goal, num_of_disrot):
    logo = pygame.image.load(logo_image)
    logo = pygame.transform.scale(logo, (logo_w, logo_h))
    screen.blit(background, (0,0))
    pygame.draw.line(screen, ui_variables.red_b, [w_2, h_1], [w_2 + temp, h_1], 5)
    pygame.draw.line(screen, ui_variables.red_b, [w_2, h_1], [w_2, h_1 + temp], 5)
    pygame.draw.line(
        screen, ui_variables.red_b, [w_2 + temp, h_1], [w_2 + temp, h_1 + temp], 5
    )
    pygame.draw.line(
        screen, ui_variables.red_b, [w_2, h_1 + temp], [w_2 + temp, h_1 + temp], 5
    )

    # Draw sidebar and background
    # if num_of_disrot == 0:  # 0회전
    #     pygame.draw.rect(
    #         screen, ui_variables.white, Rect(w_1 + w_2, 0 + h_1, w_3, temp)
    #     )
    # elif num_of_disrot == 1:  # 1회전
    #     pygame.draw.rect(
    #         screen, ui_variables.white, Rect(0 + w_2, 0 + h_1 + w_1, temp, w_3)
    #     )
    # elif num_of_disrot == 2:  # 2회전
    #     pygame.draw.rect(screen, ui_variables.white, Rect(w_2, 0 + h_1, w_3, temp))
    # elif num_of_disrot == 3:  # 3회전
    #     pygame.draw.rect(screen, ui_variables.white, Rect(0 + w_2, 0 + h_1, temp, w_3))

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            if num_of_disrot == 0:
                dx = block_size + w_1 + w_2 + block_size * j
                dy = block_size * game_loc.nmino_const_y + h_1 + block_size * i
            elif num_of_disrot == 1:
                dx = w - (block_size * game_loc.nmino_const_y + w_2 + block_size * i)
                dy = block_size + h_1 + w_1 + block_size * j
            elif num_of_disrot == 2:
                dx = w - (block_size * game_loc.rot_help + w_1 + w_2 + block_size * j)
                dy = h - (block_size * game_loc.nmino_const_y + h_1 + block_size * i)
            elif num_of_disrot == 3:
                dx = block_size * game_loc.nmino_const_y + w_2 + block_size * i
                dy = h_1 + w_3 - block_size * game_loc.rot_help - block_size * j
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size),
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold != -1:
        for i in range(4):
            for j in range(4):
                if num_of_disrot == 0:
                    dx = block_size + w_1 + w_2 + block_size * j
                    dy = block_size * game_loc.hmino_const_y + h_1 + block_size * i
                elif num_of_disrot == 1:
                    dx = w - (
                        block_size * game_loc.hmino_const_y + w_2 + block_size * i
                    )
                    dy = block_size + h_1 + w_1 + block_size * j
                elif num_of_disrot == 2:
                    dx = w - (
                        block_size * game_loc.rot_help + w_1 + w_2 + block_size * j
                    )
                    dy = h - (
                        block_size * game_loc.hmino_const_y + h_1 + block_size * i
                    )
                elif num_of_disrot == 3:
                    dx = block_size * game_loc.hmino_const_y + w_2 + block_size * i
                    dy = h_1 + w_3 - block_size * game_loc.rot_help - block_size * j
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
    if num_of_disrot == 0:
        deg = 0  # 0회전 = 0
    if num_of_disrot == 1:
        deg = 270  # 1회전 =270도
    if num_of_disrot == 2:
        deg = 180  # 2회전 = 180도
    if num_of_disrot == 3:
        deg = 90  # 3회전 = 90도
    text_hold = pygame.transform.rotate(
        ui_variables.h5.render("HOLD", 1, ui_variables.white), deg
    )
    text_next = pygame.transform.rotate(
        ui_variables.h5.render("NEXT", 1, ui_variables.white), deg
    )
    text_score = pygame.transform.rotate(
        ui_variables.h5.render("SCORE", 1, ui_variables.white), deg
    )
    score_value = pygame.transform.rotate(
        ui_variables.h4.render(str(score), 1, ui_variables.white), deg
    )
    text_level = pygame.transform.rotate(
        ui_variables.h5.render("LEVEL", 1, ui_variables.white), deg
    )
    level_value = pygame.transform.rotate(
        ui_variables.h4.render(str(level), 1, ui_variables.white), deg
    )
    text_goal = pygame.transform.rotate(
        ui_variables.h5.render("GOAL", 1, ui_variables.white), deg
    )
    goal_value = pygame.transform.rotate(
        ui_variables.h4.render(str(goal), 1, ui_variables.white), deg
    )
    logo = pygame.transform.rotate(logo, deg)


    # Place texts
    if num_of_disrot == 0:
        screen.blit(
            text_hold,
            (block_size + w_1 + w_2, block_size * game_loc.holdt_const_y + h_1),
        )
        screen.blit(
            text_next,
            (block_size + w_1 + w_2, block_size * game_loc.nextt_const_y + h_1),
        )
        screen.blit(
            text_score,
            (block_size + w_1 + w_2, block_size * game_loc.scoret_const_y + h_1),
        )
        screen.blit(
            score_value,
            (block_size + w_1 + w_2, block_size * game_loc.scorev_const_y + h_1),
        )
        screen.blit(
            text_level,
            (block_size + w_1 + w_2, block_size * game_loc.levelt_const_y + h_1),
        )
        screen.blit(
            level_value,
            (block_size + w_1 + w_2, block_size * game_loc.levelv_const_y + h_1),
        )
        screen.blit(
            text_goal,
            (block_size + w_1 + w_2, block_size * game_loc.goalt_const_y + h_1),
        )
        screen.blit(
            goal_value,
            (block_size + w_1 + w_2, block_size * game_loc.goalv_const_y + h_1),
        )
        screen.blit(logo, (block_size + w_1 + w_2, block_size * game_loc.holdt_const_y))
    
    if num_of_disrot == 1:
        screen.blit(
            text_hold,
            (w - (block_size * game_loc.holdt_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            text_next,
            (w - (block_size * game_loc.nextt_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            text_score,
            (w - (block_size * game_loc.scoret_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            score_value,
            (w - (block_size * game_loc.scorev_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            text_level,
            (w - (block_size * game_loc.levelt_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            level_value,
            (w - (block_size * game_loc.levelv_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            text_goal,
            (w - (block_size * game_loc.goalt_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(
            goal_value,
            (w - (block_size * game_loc.goalv_const_y + w_2), block_size + h_1 + w_1),
        )
        screen.blit(logo, (w - (block_size * game_loc.holdt_const_y + w_2), block_size + h_1 + w_1))
        

    if num_of_disrot == 2:
        screen.blit(
            text_hold,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.holdt_const_y + h_1),
            ),
        )
        screen.blit(
            text_next,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.nextt_const_y + h_1),
            ),
        )
        screen.blit(
            text_score,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.scoret_const_y + h_1),
            ),
        )
        screen.blit(
            score_value,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.scorev_const_y + h_1),
            ),
        )
        screen.blit(
            text_level,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.levelt_const_y + h_1),
            ),
        )
        screen.blit(
            level_value,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.levelv_const_y + h_1),
            ),
        )
        screen.blit(
            text_goal,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.goalt_const_y + h_1),
            ),
        )
        screen.blit(
            goal_value,
            (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.goalv_const_y + h_1),
            ),
        )
        screen.blit(logo, (
                w - (block_size * game_loc.rot_help + w_1 + w_2),
                h - (block_size * game_loc.holdt_const_y + h_1),
            ))

    if num_of_disrot == 3:
        screen.blit(
            text_hold,
            (
                block_size * game_loc.holdt_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            text_next,
            (
                block_size * game_loc.nextt_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            text_score,
            (
                block_size * game_loc.scoret_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            score_value,
            (
                block_size * game_loc.scorev_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            text_level,
            (
                block_size * game_loc.levelt_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            level_value,
            (
                block_size * game_loc.levelv_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            text_goal,
            (
                block_size * game_loc.goalt_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(
            goal_value,
            (
                block_size * game_loc.goalv_const_y + w_2,
                h_1 + w_3 - block_size * game_loc.rot_help,
            ),
        )
        screen.blit(logo, (block_size * game_loc.holdt_const_y + 2*(w_1 - w_3), w_3 - block_size * game_loc.rot_help,
            ))
        

    # Draw board 칸그리기
    for x in range(width):
        for y in range(height):
            if num_of_disrot == 0:  # 0회전
                dx = block_size + w_2 + block_size * x
                dy = block_size + h_1 + block_size * y
            elif num_of_disrot == 1:  # 1회전 = 270도 회전
                dx = block_size + w_2 + block_size * (height - y - 1)
                dy = block_size + h_1 + block_size * x
            elif num_of_disrot == 2:  # 2회전 = 180도 회전
                dx = block_size + w_2 + w_3 + block_size * (width - x - 1)
                dy = block_size + h_1 + block_size * (height - y - 1)
            elif num_of_disrot == 3:  # 3회전 = 90도 회전
                dx = block_size + w_2 + block_size * y
                dy = block_size + h_1 + w_3 + block_size * (width - x - 1)

            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])


##############################################################################


#######################################loop 모듈함수##########################
def PauseScreen():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause, num_of_disrot
    global dx2, dy2, rotation2, score2, level2, goal2, hard_drop2, bottom_count2, mino2, next_mino2, hold2, hold_mino2, board_state, locx, locy
    global gamemode_1, gamemode_2, gamemode_3, gamemode_4
    global matrix, matrix2
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == QUIT:
            done = True

        elif event.type == USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 300)
            if gamemode_1:
                draw_board(next_mino, hold_mino, score, level, goal)
            elif gamemode_2:
                draw_board_b(next_mino, hold_mino, score, level, goal)
            elif gamemode_3:
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)

            screen.fill(ui_variables.black)
            screen.blit(pau, (0, 0))
            goto_bnt.draw(screen, (0, 0))
            esc_bnt.draw(screen, (0,0))
            sound_bnt.draw(screen, (0,   0))
            on_bnt.draw(screen, (0,   0))
            off_bnt.draw(screen, (0,   0))
            slash_bnt.draw(screen, (0,   0))
            pygame.display.update()

        elif event.type == pygame.MOUSEMOTION:
            if goto_bnt.isOver_2(pos):
                goto_bnt.text = text14
            else:
                goto_bnt.text = text13

            if off_bnt.isOver_2(pos):
                off_bnt.text = text19
            else:
                off_bnt.text = text18


            if on_bnt.isOver_2(pos):
                on_bnt.text = text17
            else:
                on_bnt.text = text16



        elif event.type == pygame.MOUSEBUTTONDOWN:
            if goto_bnt.isOver_2(pos):
                ui_variables.click_sound.play()
                # main loop 옵션 초기화
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
                matrix = [
                    [0 for y in range(height + 1)] for x in range(width)
                ]  # height
                ##### board2 초기화
                dx2, dy2 = 3, 0
                rotation2 = 0
                num_of_disrot = 0

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

                board_state = True  # True 일때 board 1, False일때 board 2
                locx = 0
                locy = 0

                gamemode_1 = False
                gamemode_2 = False
                gamemode_3 = False
                gamemode_4 = False
                start = False
                pause = False
                popup = False
            if on_bnt.isOver_2(pos):
                ui_variables.click_sound.play()
                pygame.mixer.music.unpause()
            if off_bnt.isOver_2(pos):
                ui_variables.click_sound.play()
                pygame.mixer.music.pause()
        elif event.type == KEYDOWN:
            erase_mino(dx, dy, mino, rotation)
            if event.key == K_ESCAPE:
                pause = False
                ui_variables.click_sound.play()
                pygame.time.set_timer(pygame.USEREVENT, 1)
                if gamemode_4 : screen.fill(ui_variables.black)

def original_mode():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause
    
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            
            # Set speed
            if not game_over:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[game_key[num_of_disrot][2]]:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                else:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

            # Draw a mino
            draw_mino(dx, dy, mino, rotation)
            draw_board(next_mino, hold_mino, score, level, goal)

            # Erase a mino
            if not game_over:
                erase_mino(dx, dy, mino, rotation)

            # Move mino down
            if not is_bottom(dx, dy, mino, rotation):
                dy += 1

            # Create new mino
            else:
                if hard_drop or bottom_count == 6:
                    hard_drop = False
                    bottom_count = 0
                    score += 10 * level
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
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
                hard_drop = True
                pygame.time.set_timer(pygame.USEREVENT, 1)
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
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
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
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
                draw_board(next_mino, hold_mino, score, level, goal)
            # Move left
            elif event.key == game_key[num_of_disrot][1]:
                if not is_leftedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
            # Move right
            elif event.key == game_key[num_of_disrot][0]:
                if not is_rightedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)

    pygame.display.update()


def blackout_mode():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause
    global locy, locx, num_of_disrot

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            # Set speed
            if not game_over:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[game_key[num_of_disrot][2]]:
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
                locy -= block_size

            # Create new mino
            else:
                if hard_drop or bottom_count == 6:
                    hard_drop = False
                    bottom_count = 0
                    score += 10 * level
                    locy = 0
                    locx = 0
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
                    locy -= block_size
                    locx = 0
                hard_drop = True
                pygame.time.set_timer(pygame.USEREVENT, 1)
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Hold
            elif event.key == K_LSHIFT or event.key == K_c:
                if hold == False:
                    locx = 0
                    locy = 0
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

            # Move left
            elif event.key == K_LEFT:
                if not is_leftedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                    locx += block_size
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)
            # Move right
            elif event.key == K_RIGHT:
                if not is_rightedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                    locx -= block_size
                draw_mino(dx, dy, mino, rotation)
                draw_board_b(next_mino, hold_mino, score, level, goal)

    pygame.display.update()


def dualscreen_mode():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause
    global dx2, dy2, rotation2, score2, level2, goal2, hard_drop2, bottom_count2, mino2, next_mino2, hold2, hold_mino2, board_state


    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            # Set speed
            if not game_over:
                pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
                # keys_pressed = pygame.key.get_pressed()  #임시로 막아 놓음.
                # if keys_pressed[K_DOWN]:
                #     pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                # else:
                #     pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

            # Draw a mino

            if board_state == True:
                pygame.draw.line(screen, ui_variables.cyan, [w_4, h_1*0.9], [w_4 + w_1 , h_1*0.9], 7)

                # )  # 처음 true일때 한번 바꿔주고 시작
            draw_mino(dx, dy, mino, rotation)
            draw_mino2(dx2, dy2, mino2, rotation2)
            ##board 두개 그리
            # draw_multiboard(next_mino, hold_mino, score, level ,goal, next_mino2, hold_mino2)
            draw_board1(next_mino, hold_mino, score, level, goal)
            draw_board2(next_mino2, hold_mino2, score, level, goal)
            draw_dual_sidebar(block_size, next_mino, hold_mino, next_mino2, hold_mino2)
            # Erase a mino
            if not game_over:
                erase_mino(dx, dy, mino, rotation)
                erase_mino2(dx2, dy2, mino2, rotation2)
            # Move mino down  +  Create new mino
            # 보드 1
            if not is_bottom(dx, dy, mino, rotation):
                dy += 1  # 파이게임 좌표는 왼쪽 상단에서 0,0
            else:
                if hard_drop or bottom_count == 6:
                    hard_drop = False
                    bottom_count = 0
                    score += 10 * level
                    draw_mino(dx, dy, mino, rotation)

                    draw_board1(next_mino, hold_mino, score, level, goal)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )
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

            # 보드 2
            if not is_bottom2(dx2, dy2, mino2, rotation2):
                dy2 += 1  # 파이게임 좌표는 왼쪽 상단에서 0,0
            else:
                if hard_drop2 or bottom_count2 == 6:
                    hard_drop2 = False
                    bottom_count2 = 0
                    score2 += 10 * level2
                    draw_mino2(dx2, dy2, mino2, rotation2)
                    draw_board2(next_mino2, hold_mino2, score, level, goal)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )

                    if is_stackable2(next_mino2):
                        mino2 = next_mino2
                        next_mino2 = randint(1, 7)
                        dx2, dy2 = 3, 0
                        rotation2 = 0
                        hold2 = False
                    else:
                        start = False
                        game_over = True
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

            # board2
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
            erase_mino(dx, dy, mino, rotation)
            erase_mino2(dx2, dy2, mino2, rotation2)

            if event.key == K_ESCAPE:
                ui_variables.click_sound.play()
                pause = True
            elif event.key == K_TAB:  # board_state로 플레히는 board 전환
                if board_state == True:  # 보드 다시 한번 그려주기
                    screen.fill(ui_variables.black)
                    pygame.draw.line(screen, ui_variables.black, [w_4, h_1*game_loc.d_draw_const], [w_4 + w_1 , h_1*game_loc.d_draw_const], 7)
                    pygame.draw.line(screen, ui_variables.cyan, [w_4+w_1, h_1*game_loc.d_draw_const], [w_4 + w_1*2 , h_1*game_loc.d_draw_const], 7)

                    draw_board1(next_mino, hold_mino, score, level, goal)
                    draw_board2(next_mino2, hold_mino2, score2, level2, goal2)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino2(dx2, dy2, mino2, rotation2)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )
                    board_state = not board_state  # 반전시키는 부분
                else:
                    screen.fill(ui_variables.black)
                    pygame.draw.line(screen, ui_variables.black, [w_4+w_1, h_1*game_loc.d_draw_const], [w_4 + w_1*2 , h_1*game_loc.d_draw_const], 7)
                    pygame.draw.line(screen, ui_variables.cyan, [w_4, h_1*game_loc.d_draw_const], [w_4 + w_1 , h_1*game_loc.d_draw_const], 7)
                    board_state = not board_state  # 반전시키는 부분
                    draw_board1(next_mino, hold_mino, score, level, goal)
                    draw_board2(next_mino2, hold_mino2, score, level, goal)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino2(dx2, dy2, mino2, rotation2)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )

            elif event.key == K_SPACE:
                ui_variables.drop_sound.play()
                if board_state == True:
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board1(next_mino, hold_mino, score, level, goal)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )
                else:
                    while not is_bottom2(dx2, dy2, mino2, rotation2):
                        dy2 += 1
                    hard_drop2 = True
                    draw_mino2(dx2, dy2, mino2, rotation2)
                    draw_board2(next_mino2, hold_mino2, score, level, goal)
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )

            # Hold
            elif event.key == K_LSHIFT or event.key == K_c:
                if board_state == True:
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
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )
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
                    draw_dual_sidebar(
                        block_size, next_mino, hold_mino, next_mino2, hold_mino2
                    )

            # Turn right
            elif event.key == K_x:
                if board_state == True:
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
                if board_state == True:
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
                if board_state == True:
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


def rotate_mode():
    global game_over, framerate, dx, dy, score, level, goal, bottom_count, hard_drop
    global rotation, mino, next_mino, hold, hold_mino, name, name_location, blink, start, done, pause
    global locy, locx, num_of_disrot
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == USEREVENT:
            # Set speed
            if not game_over:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[game_key[num_of_disrot][2]]:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                else:
                    pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

            # Draw a mino
            draw_mino(dx, dy, mino, rotation)
            draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)

            # Erase a mino
            if not game_over:
                erase_mino(dx, dy, mino, rotation)

            # Move mino down
            if not is_bottom(dx, dy, mino, rotation):
                dy += 1
                locy -= block_size

            # Create new mino
            else:
                if hard_drop or bottom_count == 6:
                    hard_drop = False
                    bottom_count = 0
                    score += 10 * level
                    locx = 0
                    locy = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )
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
                    locy -= block_size
                hard_drop = True
                pygame.time.set_timer(pygame.USEREVENT, 1)
                draw_mino(dx, dy, mino, rotation)
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)
            # Hold
            elif event.key == K_LSHIFT or event.key == K_c:
                locx = 0
                locy = 0
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
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)
            # Turn right
            elif event.key == K_x:
                if is_turnable_l(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    num_of_disrot += 1
                    rotation -= 1
                # Kick
                elif is_turnable_l(dx, dy - 1, mino, rotation):
                    ui_variables.move_sound.play()
                    dy -= 1
                    num_of_disrot += 1
                    rotation -= 1
                elif is_turnable_l(dx + 1, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                    num_of_disrot += 1
                    rotation -= 1
                elif is_turnable_l(dx - 1, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                    num_of_disrot += 1
                    rotation -= 1
                elif is_turnable_l(dx, dy - 2, mino, rotation):
                    ui_variables.move_sound.play()
                    dy -= 2
                    num_of_disrot += 1
                    rotation -= 1
                elif is_turnable_l(dx + 2, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 2
                    num_of_disrot += 1
                    rotation -= 1
                elif is_turnable_l(dx - 2, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 2
                    num_of_disrot += 1
                    rotation -= 1
                if num_of_disrot == 4:
                    num_of_disrot = 0
                if rotation == -1:
                    rotation = 3
                draw_mino(dx, dy, mino, rotation)
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)
            # Move left
            elif event.key == game_key[num_of_disrot][1]:
                if not is_leftedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx -= 1
                    locx += block_size
                draw_mino(dx, dy, mino, rotation)
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)
            # Move right
            elif event.key == game_key[num_of_disrot][0]:
                if not is_rightedge(dx, dy, mino, rotation):
                    ui_variables.move_sound.play()
                    dx += 1
                    locx -= block_size
                draw_mino(dx, dy, mino, rotation)
                draw_board_r(next_mino, hold_mino, score, level, goal, num_of_disrot)

    pygame.display.update()


#############################################################################
pygame.init()
pygame.mixer.music.load("assets/sounds/background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)


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


def ranking_sort():
    with open("leaderboard.txt") as f:
        lines = f.readlines()

    lines = [line.rstrip("\n") for line in open("leaderboard.txt")]

    leaders_o = {}
    leaders_b = {}
    leaders_r = {}
    leaders_d = {}

    for line in lines:
        mode_temp = line.split(" ")[0]
        score_temp = line.split(" ")[1]
        if mode_temp[0] == "o":
            leaders_o[mode_temp[1:]] = int(score_temp)
        elif mode_temp[0] == "b":
            leaders_b[mode_temp[1:]] = int(score_temp)
        elif mode_temp[0] == "r":
            leaders_r[mode_temp[1:]] = int(score_temp)
        elif mode_temp[0] == "d":
            leaders_d[mode_temp[1:]] = int(score_temp)

    # make each leaders as sorted list
    leaders_o = sorted(leaders_o.items(), key=operator.itemgetter(1), reverse=True)
    leaders_b = sorted(leaders_b.items(), key=operator.itemgetter(1), reverse=True)
    leaders_r = sorted(leaders_r.items(), key=operator.itemgetter(1), reverse=True)
    leaders_d = sorted(leaders_d.items(), key=operator.itemgetter(1), reverse=True)

    with open("leaderboard.txt", "w") as f:
        for info in leaders_o:
            f.write("o" + info[0] + " " + str(info[1]) + "\n")
        for info in leaders_b:
            f.write("b" + info[0] + " " + str(info[1]) + "\n")
        for info in leaders_r:
            f.write("r" + info[0] + " " + str(info[1]) + "\n")
        for info in leaders_d:
            f.write("d" + info[0] + " " + str(info[1]) + "\n")

    return leaders_o[:5], leaders_b[:5], leaders_r[:5], leaders_d[:5]


def ranking():
    o, b, r, d = ranking_sort()
    o_text = []
    b_text = []
    r_text = []
    d_text = []
    for item in o:
        o_text.append(
            (
                ui_variables.h4.render(item[0], 1, ui_variables.white),
                (ui_variables.h4.render(str(item[1]), 1, ui_variables.white)),
            )
        )
    for item in b:
        b_text.append(
            (
                ui_variables.h4.render(item[0], 1, ui_variables.white),
                (ui_variables.h4.render(str(item[1]), 1, ui_variables.white)),
            )
        )
    for item in r:
        r_text.append(
            (
                ui_variables.h4.render(item[0], 1, ui_variables.white),
                (ui_variables.h4.render(str(item[1]), 1, ui_variables.white)),
            )
        )
    for item in d:
        d_text.append(
            (
                ui_variables.h4.render(item[0], 1, ui_variables.white),
                (ui_variables.h4.render(str(item[1]), 1, ui_variables.white)),
            )
        )

    screen.blit(
        ui_variables.h2.render("Original", 1, ui_variables.white),
        (rank_w, temp / 2),
    )
    for item in o_text:
        screen.blit(
            item[0],
            (
                rank_w,
                temp / 2
                + game_loc.rank_blank_y * block_size * (o_text.index(item) + 1),
            ),
        )
        screen.blit(
            item[1],
            (
                rank_w + game_loc.rank_info_blank * block_size,
                temp / 2
                + game_loc.rank_blank_y * block_size * (o_text.index(item) + 1),
            ),
        )
    screen.blit(
        ui_variables.h2.render("Blackout", 1, ui_variables.white),
        (rank_w + game_loc.rank_mode_blank * block_size, temp / 2),
    )
    for item in b_text:
        screen.blit(
            item[0],
            (
                rank_w + game_loc.rank_mode_blank * block_size,
                temp / 2
                + game_loc.rank_blank_y * block_size * (b_text.index(item) + 1),
            ),
        )
        screen.blit(
            item[1],
            (
                rank_w
                + game_loc.rank_mode_blank * block_size
                + game_loc.rank_info_blank * block_size,
                temp / 2
                + game_loc.rank_blank_y * block_size * (b_text.index(item) + 1),
            ),
        )
    screen.blit(
        ui_variables.h2.render("Rotate", 1, ui_variables.white),
        (rank_w + game_loc.rank_mode_blank * block_size * 2, temp / 2),
    )
    for item in r_text:
        screen.blit(
            item[0],
            (
                rank_w + game_loc.rank_mode_blank * block_size * 2,
                temp / 2
                + game_loc.rank_blank_y * block_size * (r_text.index(item) + 1),
            ),
        )
        screen.blit(
            item[1],
            (
                rank_w
                + game_loc.rank_mode_blank * block_size * 2
                + game_loc.rank_info_blank * block_size,
                temp / 2
                + game_loc.rank_blank_y * block_size * (r_text.index(item) + 1),
            ),
        )
    screen.blit(
        ui_variables.h2.render("Dual", 1, ui_variables.white),
        (rank_w + game_loc.rank_mode_blank * block_size * 3, temp / 2),
    )
    for item in d_text:
        screen.blit(
            item[0],
            (
                rank_w + game_loc.rank_mode_blank * block_size * 3,
                temp / 2
                + game_loc.rank_blank_y * block_size * (d_text.index(item) + 1),
            ),
        )
        screen.blit(
            item[1],
            (
                rank_w
                + game_loc.rank_mode_blank * block_size * 3
                + game_loc.rank_info_blank * block_size,
                temp / 2
                + game_loc.rank_blank_y * block_size * (d_text.index(item) + 1),
            ),
        )


"""
with open("leaderboard.txt") as f:
    lines = f.readlines()
lines = [line.rstrip("\n") for line in open("leaderboard.txt")]

leaders = {"AAA": 0, "BBB": 0, "CCC": 0}
for i in lines:
    leaders[i.split(" ")[0]] = int(i.split(" ")[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
"""
matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
################## 추가된 initial value  ######################################
dx2, dy2 = 3, 0
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

board_state = True  # True 일때 board 1, False일때 board 2

game_key = (  # 좌, 우, 소프트 드롭
    (K_RIGHT, K_LEFT, K_DOWN),
    (K_DOWN, K_UP, K_LEFT),
    (K_LEFT, K_RIGHT, K_UP),
    (K_UP, K_DOWN, K_RIGHT),
)


locx = 0  # for move left, right
locy = 0  # for move up, down
num_of_disrot = 0
###########################################################


# 게임모드
gamemode_1 = False  # original
gamemode_2 = False  # blackout
gameode_3 = False  # rotate
gmaemode_4 = False  # dualscreen


###########################################################
# Loop Start
###########################################################
while not done:
    update_display()
    # Pause screen
    if pause:
        PauseScreen()
    # Game screen
    elif start:
        if gamemode_1:
            original_mode()
        if gamemode_2:
            blackout_mode()
        elif gamemode_3:
            rotate_mode()
        elif gamemode_4:
            dualscreen_mode()
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

                # draw_multiboard(next_mino, hold_mino, score, level ,goal, next_mino2, hold_mino2)
                if gamemode_1:
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif gamemode_2:
                    draw_board_b(next_mino, hold_mino, score, level, goal)
                elif gamemode_3:
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )
                elif gamemode_4:
                    draw_board1(next_mino, hold_mino, score, level, goal)
                    draw_board2(next_mino2, hold_mino2, score, level, goal)

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
                    if gamemode_1:
                        outfile = open("leaderboard.txt", "a")
                        outfile.write(
                            chr(111)
                            + chr(name[0])
                            + chr(name[1])
                            + chr(name[2])
                            + " "
                            + str(score)
                            + "\n"
                        )
                        outfile.close()
                    elif gamemode_2:
                        outfile = open("leaderboard.txt", "a")
                        outfile.write(
                            chr(98)
                            + chr(name[0])
                            + chr(name[1])
                            + chr(name[2])
                            + " "
                            + str(score)
                            + "\n"
                        )
                    elif gamemode_3:
                        outfile = open("leaderboard.txt", "a")
                        outfile.write(
                            chr(114)
                            + chr(name[0])
                            + chr(name[1])
                            + chr(name[2])
                            + " "
                            + str(score)
                            + "\n"
                        )
                    elif gamemode_4:
                        outfile = open("leaderboard.txt", "a")
                        outfile.write(
                            chr(100)
                            + chr(name[0])
                            + chr(name[1])
                            + chr(name[2])
                            + " "
                            + str(score + score2)
                            + "\n"
                        )

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score2 = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [
                        [0 for y in range(height + 1)] for x in range(width)
                    ]  # height
                    ##### board2 초기화
                    dx2, dy2 = 3, 0
                    rotation2 = 0
                    num_of_disrot = 0

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

                    board_state = True  # True 일때 board 1, False일때 board 2
                    locx = 0
                    locy = 0

                    gamemode_1 = False
                    gamemode_2 = False
                    gamemode_3 = False
                    gamemode_4 = False
                    start = False
                    pause = False
                    popup = False
                    #############

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
    # popuop
    elif popup:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                screen.blit(howtoplay, (0, 0))
                goto_bnt.draw(screen, (0, 0, 0))
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if goto_bnt.isOver_2(pos):
                    goto_bnt.text = text14
                else:
                    goto_bnt.text = text13
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if goto_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    popup = False
    # Start screen
    else:
        # pygame.time.set_timer(pygame.USEREVENT, 300)
        screen.fill(ui_variables.black)
        screen.blit(main, (0, 0))

        origianl_bnt.draw(screen, (0, 0, 0))
        rotate_bnt.draw(screen, (0, 0, 0))
        dual_bnt.draw(screen, (0, 0, 0))
        blackout_bnt.draw(screen, (0, 0, 0))
        info_bnt.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                if origianl_bnt.isOver_2(pos):
                    origianl_bnt.text = text2
                else:
                    origianl_bnt.text = text1
                if rotate_bnt.isOver_2(pos):
                    rotate_bnt.text = text4
                else:
                    rotate_bnt.text = text3
                if dual_bnt.isOver_2(pos):
                    dual_bnt.text = text6
                else:
                    dual_bnt.text = text5
                if blackout_bnt.isOver_2(pos):
                    blackout_bnt.text = text8
                else:
                    blackout_bnt.text = text7
                if info_bnt.isOver_2(pos):
                    info_bnt.text = text10
                else:
                    info_bnt.text = text9

            elif event.type == pygame.MOUSEBUTTONDOWN:  # 순서가 좀 꼬인 듯함
                if origianl_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_1 = True
                    start = True
                if rotate_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gamemode_2 = True
                    # gamemode_3 = True
                if dual_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gamemode_3 = True
                if blackout_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gamemode_4 = True
                    screen.fill(ui_variables.black)

                if info_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    popup = True

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
