import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supplies
from random import *

pygame.init()

# initialize the mixer module for Sound loading and playback
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Plane War!!")

bg_image = pygame.image.load("images/background.png").convert_alpha()

# all the sounds in the game
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound("sound/button.wav")
button_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.5)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
use_bomb_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)

# color RGBs
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# create "start again" and "end game" images
# convert_alpha() creates a new surface that will be in a format suited for quick blitting to the given format with per pixel alpha
again_image = pygame.image.load('images/again.png').convert_alpha()
again_rect = again_image.get_rect()
end_game_image = pygame.image.load('images/end_game.png').convert_alpha()
end_game_rect = end_game_image.get_rect()


# create small enemies
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


# create mid enemies
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


# create large enemies
def add_large_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def inc_speed(group, increment):
    for each in group:
        each.speed += increment


def create_again_endgame(again_rect, end_game_rect):
    # show the "start again" and "end game" button
    screen.blit(again_image, again_rect)
    screen.blit(end_game_image, end_game_rect)

    # pygame.mouse.get_pressed() returns a list of boolean values representing the states of the buttons
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
            main()
        elif end_game_rect.left < pos[0] < end_game_rect.right and end_game_rect.top < pos[1] < end_game_rect.bottom:
            pygame.quit()
            sys.exit()


def main():
    # play background music
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    running = True

    me = myplane.MyPlane(bg_size)

    # produce enemies
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)

    # produce regular bullets
    BULLET1_NUM = 4
    bullet1 = []
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # produce super bullets
    is_double_bullet = False
    BULLET2_NUM = 8
    bullet2 = []
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    delay = 100

    e1_index = 0
    e2_index = 0
    e3_index = 0
    me_index = 0
    bullet1_index = 0
    bullet2_index = 0

    count = 0
    font = pygame.font.Font("font/font.ttf", 36)

    # about pause button
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    control_rect = pause_nor_image.get_rect()
    control_image = pause_nor_image
    # set the position of the control button
    control_rect.left, control_rect.top = width - control_rect.width - 10, 10
    pause = False

    # initialize level to 1 at first
    level = 1

    # about bomb
    bomb = False
    bomb_number = 3
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left, bomb_rect.top = 10, height - bomb_rect.height - 10
    bomb_font = pygame.font.Font("font/font.ttf", 48)

    # about supplies
    bomb_supply = supplies.BombSupply(bg_size)
    bullet_supply = supplies.BulletSupply(bg_size)
    # USEREVENT is used to create a new event ID which is 24
    # there are 32 ID slots in total , and the first 23 ID slots are predefined to be pygame events
    SUPPLY_TIME = USEREVENT
    # drop supply every 30 secs
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
    DOUBLE_BULLET_SUPPLY = USEREVENT + 1

    # about lives
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_rect.left, life_rect.top = width - 56, height - 67
    life_num = 3
    INVINCIBLE_TIME = USEREVENT + 2

    # initialize best score and whether or not it is recorded in the document
    best_score = 0
    recorded = False

    while running:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                # if the pause button is pressed
                # however, this happens only when the mouse is clicked
                if event.button == 1 and control_rect.collidepoint(event.pos):
                    pause = not pause
                    if pause:
                        # disable the timer for the SUPPLY_TIME event by setting the second argument to be 0
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.pause()
                        pygame.mixer.music.pause()
                        control_image = resume_pressed_image
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.unpause()
                        pygame.mixer.music.unpause()
                        control_image = pause_pressed_image

            elif event.type == MOUSEMOTION:
                # if the mouse hovers over the pause button, change the button to the pressed ones
                if control_rect.collidepoint(event.pos):
                    if pause:
                        control_image = resume_pressed_image
                    else:
                        control_image = pause_pressed_image
                else:
                    if pause:
                        control_image = resume_nor_image
                    else:
                        control_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_number:
                        use_bomb_sound.play()
                        bomb_number -= 1
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            # drop the supplies (could be bombs or extra bullets)
            elif event.type == SUPPLY_TIME:
                if not pause:
                    supply_sound.play()
                    # randomly choose whether the supply is gonna be bombs or bullets
                    if choice([True, False]):
                        bomb_supply.reset()
                    else:
                        bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_SUPPLY:
                pygame.time.set_timer(DOUBLE_BULLET_SUPPLY, 0)
                is_double_bullet = False

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # ==================== if still alive ===================
        if life_num:
            # draw pause button
            screen.blit(control_image, control_rect)

            # -------------------- if the game is not paused -----------------
            if not pause:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    me.moveLeft()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    me.moveRight()
                if key_pressed[K_w] or key_pressed[K_UP]:
                    me.moveUp()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    me.moveDown()

                # launch bullets every 10 frames
                if not (delay % 10):
                    if is_double_bullet:
                        bullet2[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                        bullet2[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                        bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                    else:
                        bullet1[bullet1_index].reset(me.rect.midtop)
                        bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                # draw bullets:
                for each in bullet1:
                    if each.active:
                        each.move()
                        screen.blit(each.image, each.rect)
                        # check if enemies are hit by any of the bullet
                        collide = pygame.sprite.spritecollide(each, enemies, False, pygame.sprite.collide_mask)
                        if collide:
                            each.active = False
                            for item in collide:
                                if item in mid_enemies or item in large_enemies:
                                    item.energy -= 1
                                    item.hit = True
                                    if item.energy == 0:
                                        item.active = False
                                else:
                                    item.active = False

                for each in bullet2:
                    if each.active:
                        each.move()
                        screen.blit(each.image, each.rect)
                        # check if enemies are hit by any of the bullet
                        collide = pygame.sprite.spritecollide(each, enemies, False, pygame.sprite.collide_mask)
                        if collide:
                            each.active = False
                            for item in collide:
                                if item in mid_enemies or item in large_enemies:
                                    item.energy -= 1
                                    item.hit = True
                                    if item.energy == 0:
                                        item.active = False
                                else:
                                    item.active = False

                # draw bomb_supply
                if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image, bomb_supply.rect)
                    if pygame.sprite.collide_mask(me, bomb_supply):
                        get_bomb_sound.play()
                        bomb_supply.active = False
                        if bomb_number < 3:
                            bomb_number += 1

                # draw bullet_supply
                if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image, bullet_supply.rect)
                    if pygame.sprite.collide_mask(me, bullet_supply):
                        get_bullet_sound.play()
                        bullet_supply.active = False
                        pygame.time.set_timer(DOUBLE_BULLET_SUPPLY, 18 * 1000)
                        is_double_bullet = True

                # draw large enemies
                for each in large_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                        else:
                            if not (delay % 5):
                                screen.blit(each.image1, each.rect)
                            else:
                                screen.blit(each.image2, each.rect)

                        # blood indicator
                        pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5), 2)
                        blood_remain = each.energy / enemy.LargeEnemy.energy
                        if blood_remain > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen, energy_color,
                                         (int(each.rect.left), int(each.rect.top - 5)),
                                         (int(each.rect.left + each.rect.width * blood_remain),
                                          int(each.rect.top - 5)), 2)
                        # sound effect when the large enemy is approaching
                        if each.rect.bottom == 0:
                            enemy3_flying_sound.play(-1)
                    # destroy
                    else:
                        if not (delay % 3):
                            if e3_index == 0:
                                enemy3_down_sound.play()
                            screen.blit(each.destroy_images[e3_index], each.rect)
                            e3_index = (e3_index + 1) % 6
                            if e3_index == 0:
                                enemy3_flying_sound.stop()
                                each.reset()
                                count += 10000

                # draw mid enemies
                for each in mid_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                        else:
                            screen.blit(each.image, each.rect)

                        # blood indicator
                        pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                         (each.rect.right, each.rect.top - 5), 2)
                        blood_remain = each.energy / enemy.MidEnemy.energy
                        if blood_remain > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen, energy_color,
                                         (int(each.rect.left), int(each.rect.top - 5)),
                                         (int(each.rect.left + each.rect.width * blood_remain),
                                          int(each.rect.top - 5)), 2)
                    # destroy
                    else:
                        if not (delay % 3):
                            if e2_index == 0:
                                enemy2_down_sound.play()
                            screen.blit(each.destroy_images[e2_index], each.rect)
                            e2_index = (e2_index + 1) % 4
                            if e2_index == 0:
                                each.reset()
                                count += 6000

                # draw small enemies
                for each in small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image, each.rect)
                    # destroy
                    else:
                        if not (delay % 3):
                            if e1_index == 0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[e1_index], each.rect)
                            e1_index = (e1_index + 1) % 4
                            if e1_index == 0:
                                each.reset()
                                count += 1000

                # check if my plane has crashed
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down and not me.invincible:
                    me.active = False
                    for each in enemies_down:
                        each.active = False

                # my plane
                if me.active:
                    if not me.invincible:
                        if not (delay % 5):
                            screen.blit(me.image1, me.rect)
                        else:
                            screen.blit(me.image2, me.rect)
                    else:
                        if not (delay % 7):
                            screen.blit(me.image1, me.rect)
                # destroyed
                else:
                    if not (delay % 3):
                        if me_index == 0:
                            me_down_sound.play()
                        screen.blit(each.destroy_images[me_index], each.rect)
                        me_index = (me_index + 1) % 4
                        if me_index == 0:
                            life_num -= 1
                            me.reset()
                            pygame.time.set_timer(INVINCIBLE_TIME, 1 * 1000)

                # draw bombs
                screen.blit(bomb_image, bomb_rect)
                bomb_text = bomb_font.render("* %s" % bomb_number, True, (255, 255, 255))
                text_rect = bomb_text.get_rect()
                screen.blit(bomb_text, (bomb_rect.right + 15, height - text_rect.height - 5))

                # draw lives left
                for i in range(life_num):
                    screen.blit(life_image, (life_rect.left - life_rect.width * i, life_rect.top))

                # score part on the top left corner of the page
                content = "score: " + str(count)
                screen.blit(font.render(content, True, (255, 255, 255)), (10, 5))

            # ------------------------ if the game is paused ----------------------
            elif pause:
                # if the game is paused, show the "start again" and "end game" buttons
                # first create the rect for "start again" and "end game" buttons, and set their positions
                again_rect.left, again_rect.top = (width - again_rect.width) // 2, height - 400


                end_game_rect.left, end_game_rect.top = (width - end_game_rect.width) // 2, height - 310

                create_again_endgame(again_rect, end_game_rect)

        # =============================== if game is over =======================
        elif life_num == 0:
            # stop all the music
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            # stop supplies
            pygame.time.set_timer(SUPPLY_TIME, 0)
            # record the best score
            if not recorded:
                recorded = True
                with open("recorded.txt", "r") as f:
                    best_score = int(f.read())
                if count > best_score:
                    best_score = count
                    with open("recorded.txt", "w") as f:
                        f.write(str(count))

            # score texts shown in the "game over" page
            score_font = pygame.font.Font("font/font.ttf", 55)
            score_text = score_font.render("Your Score", True, (255, 255, 255))
            score_rect = score_text.get_rect()
            score_rect.left, score_rect.top = (width - score_rect.width) // 2, 200
            score2_text = score_font.render("%s" % count, True, (255, 255, 255))
            score2_rect = score2_text.get_rect()
            score2_rect.left, score2_rect.top = (width - score2_rect.width) // 2, 265

            # best score part in the "game over" page
            best_score_text = font.render("Best: %s" % best_score, True, (255, 255, 255))
            best_rect = best_score_text.get_rect()
            best_rect.left, best_rect.top = 50, 50

            # write scores after game is over
            screen.blit(best_score_text, best_rect)
            screen.blit(score_text, score_rect)
            screen.blit(score2_text, score2_rect)

            # if the game is over, create the "start again" and "end game" buttons
            again_rect.left, again_rect.top = (width - again_rect.width) // 2, height - 300
            end_game_rect.left, end_game_rect.top = (width - end_game_rect.width) // 2, height - 250
            create_again_endgame(again_rect, end_game_rect)

        # delay
        delay -= 1
        if not delay:
            delay = 100

        # different levels of the game
        if level == 1 and count >= 50000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        if level == 2 and count >= 300000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        if level == 3 and count >= 6000000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 24)
            add_mid_enemies(mid_enemies, enemies, 10)
            add_large_enemies(large_enemies, enemies, 5)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        if level == 4 and count >= 1000000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 27)
            add_mid_enemies(mid_enemies, enemies, 12)
            add_large_enemies(large_enemies, enemies, 6)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        # update the content of the entire screen
        pygame.display.flip()
        # the program will never run more than 60 frames/sec
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    else:
        traceback.print_exc()
        pygame.quit()
        input()
