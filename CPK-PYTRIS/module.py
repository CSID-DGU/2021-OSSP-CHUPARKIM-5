# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
from mino import *
from random import *
from pygame.locals import *
from game_func import *
from game_var import *

pygame.init()

###########################################################
# Loop Start
###########################################################

# test
gamemode_1 = False
gamemode_2 = False
gamemode_3 = False
gamemode_4 = False

while not done:
    # 창 Resize 감지
    update_display()
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                if gamemode_1:
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif gamemode_2:
                    draw_board_b(next_mino, hold_mino, score, level, goal, locx, locy)
                elif gamemode_3:
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )

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
                if gamemode_1:
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif gamemode_2:
                    draw_board_b(next_mino, hold_mino, score, level, goal, locx, locy)
                elif gamemode_3:
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1
                    if gamemode_2:
                        locy -= 17

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        if gamemode_2:
                            locx = 0
                            locy = 0
                        draw_mino(dx, dy, mino, rotation)
                        if gamemode_1:
                            draw_board(next_mino, hold_mino, score, level, goal)
                        elif gamemode_2:
                            draw_board_b(
                                next_mino, hold_mino, score, level, goal, locx, locy
                            )
                        elif gamemode_3:
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
                        if gamemode_2:
                            locy -= 17
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    if gamemode_1:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    elif gamemode_2:
                        draw_board_b(
                            next_mino, hold_mino, score, level, goal, locx, locy
                        )
                    elif gamemode_3:
                        draw_board_r(
                            next_mino, hold_mino, score, level, goal, num_of_disrot
                        )
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        if gamemode_2:
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
                    if gamemode_1:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    elif gamemode_2:
                        draw_board_b(
                            next_mino, hold_mino, score, level, goal, locx, locy
                        )
                    elif gamemode_3:
                        draw_board_r(
                            next_mino, hold_mino, score, level, goal, num_of_disrot
                        )
                # Turn right (else rotate mode)
                elif (not gamemode_3) and event.key == K_x:
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
                    if gamemode_1:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    elif gamemode_2:
                        draw_board_b(
                            next_mino, hold_mino, score, level, goal, locx, locy
                        )
                # Turn right (on rotate mode)
                elif gamemode_3 and event.key == K_x:
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
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )

                # Move left
                elif event.key == game_key[num_of_disrot][1]:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        if gamemode_2:
                            locx += 17
                    draw_mino(dx, dy, mino, rotation)
                    if gamemode_1:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    elif gamemode_2:
                        draw_board_b(
                            next_mino, hold_mino, score, level, goal, locx, locy
                        )
                    elif gamemode_3:
                        draw_board_r(
                            next_mino, hold_mino, score, level, goal, num_of_disrot
                        )
                # Move right
                elif event.key == game_key[num_of_disrot][0]:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        if gamemode_2:
                            locx -= 17
                    draw_mino(dx, dy, mino, rotation)
                    if gamemode_1:
                        draw_board(next_mino, hold_mino, score, level, goal)
                    elif gamemode_2:
                        draw_board_b(
                            next_mino, hold_mino, score, level, goal, locx, locy
                        )
                    elif gamemode_3:
                        draw_board_r(
                            next_mino, hold_mino, score, level, goal, num_of_disrot
                        )

        pygame.display.update()

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

                if gamemode_1:
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif gamemode_2:
                    draw_board_b(next_mino, hold_mino, score, level, goal, locx, locy)
                elif gamemode_3:
                    draw_board_r(
                        next_mino, hold_mino, score, level, goal, num_of_disrot
                    )

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

    elif gamemode_1 or gamemode_2:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                start = True

    elif gamemode_3 or gamemode_4:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                start = True

    # Start screen
    else:
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if origianl_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_1 = True
                if rotate_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_2 = True
                if dual_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_3 = True
                if blackout_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_4 = True
                if info_bnt.isOver_2(pos):
                    ui_variables.click_sound.play()
                    gamemode_1 = True

        # pygame.time.set_timer(pygame.USEREVENT, 300)
        screen.fill(ui_variables.black)
        screen.blit(main, (0, 0))

        origianl_bnt.draw(screen, (0, 0, 0))
        rotate_bnt.draw(screen, (0, 0, 0))
        dual_bnt.draw(screen, (0, 0, 0))
        blackout_bnt.draw(screen, (0, 0, 0))
        info_bnt.draw(screen, (0, 0, 0))

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
