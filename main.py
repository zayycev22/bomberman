from classes import *
import pygame
from pygame import *
from menu import *
import os
import random


def set_bomb(player):
    player.num_of_bombs += 1
    x = ((player.rect.x + 10) // 20) * 20
    y = ((player.rect.y + 10) // 20) * 20
    bomb = Bomb(x, y, 20, 20)
    all_sprite_list.add(bomb)
    player.bomb_list.add(bomb)


pygame.init()
display = pygame.display.set_mode((500, 500))
screen = pygame.display.get_surface()

"""списки обьектов"""
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()
all_players = pygame.sprite.Group()
break_list = pygame.sprite.Group()
expo_list = pygame.sprite.Group()
bonus_list = pygame.sprite.Group()

"""установка неломаемых стен"""
for i in [0, 480]:
    for j in range(0, 500, 20):
        wall = Wall(j, i, 20, 20)
        wall_list.add(wall)
        all_sprite_list.add(wall)

for i in [0, 480]:
    for j in range(20, 480, 20):
        wall = Wall(i, j, 20, 20)
        wall_list.add(wall)
        all_sprite_list.add(wall)

for i in range(40, 480, 40):
    for j in range(40, 480, 40):

        wall = Wall(i, j, 20, 20)
        wall_list.add(wall)
        all_sprite_list.add(wall)


"""отрисовка ломаемых стен"""
for i in range(60, 460, 40):
    for j in range(40, 460, 20):
        a = random.randint(0, 5)
        if a != 1:
            wall = Break(i, j, 20, 20)
            break_list.add(wall)
            all_sprite_list.add(wall)

for i in range(40, 480, 40):
    for j in range(60, 460, 40):
        a = random.randint(0, 5)
        if a != 0:
            wall = Break(i, j, 20, 20)
            break_list.add(wall)
            all_sprite_list.add(wall)

for i in [20, 460]:
    for j in range(60, 440, 20):
        a = random.randint(0, 15)
        if a != 0:
            wall = Break(i, j, 20, 20)
            break_list.add(wall)
            all_sprite_list.add(wall)
            wall = Break(j, i, 20, 20)
            break_list.add(wall)
            all_sprite_list.add(wall)


"""какие-то переменные"""
FPS = 60
clock = pygame.time.Clock()
# 23, 23
# 463, 23
# 23, 463
# 463, 463
"""инициализация игроков"""
alive_players = 4
players = []
"""игрок 1"""
player1 = Player(23, 23, 'blue')
player1.walls = wall_list
players.append(player1)
all_players.add(player1)
all_sprite_list.add(player1)
"""игрок 2"""
player2 = Player(23, 463, 'red')
player2.walls = wall_list
players.append(player2)
all_players.add(player2)
all_sprite_list.add(player2)
"""игрок 1"""
player3 = Player(463, 23, 'purple')
player3.walls = wall_list
players.append(player3)
all_players.add(player3)
all_sprite_list.add(player3)
"""игрок 1"""
player4 = Player(463, 463, 'yellow')
player4.walls = wall_list
players.append(player4)
all_players.add(player4)
all_sprite_list.add(player4)

"""вызов меню"""
# menu()
# print(players)
ptr = 1

"""основной игровой цикл"""
done = False
while not done and alive_players > 1:
    display.fill((00, 94, 00))
    pygame.time.delay(10)

    if ptr != 0:
        ptr = menu()
    if ptr == 2:
        break
    elif ptr == 1:
        ptr_about = about()
        if ptr_about:
            done = True
        continue

    """проверка и удаление бонусов"""
    for i in bonus_list:
        if i.num_bonus == 0:
            i.kill()

    """проверка и удаление взрывов"""
    for i in expo_list:
        if i.time <= 0:
            for j in i.picture_list:
                j.kill()
            all_sprite_list.remove(i)
            expo_list.remove(i)

        for j in i.picture_list:
            j.time -= 1
        i.time -= 1

    alive_players = 0

    for player in players:
        if player.is_alive:
            alive_players += 1
        # print(bomb_list)
        player.break_list = break_list
        player.bonus_list=bonus_list

        """изменение параметров игрока бонусами"""
        if player.num_bonus == 1:
            a, b = player.speed_x, player.speed_y
            if a > 0:
                a += 0.5
            if a < 0:
                a -= 0.5
            if b > 0:
                b += 0.5
            if b < 0:
                b -= 0.5
            player.speed += 0.5
            player.num_bonus = 0
            player.speed_x, player.speed_y = a, b
        elif player.num_bonus == 2:
            player.expl_rad += 1
            player.num_bonus = 0
        elif player.num_bonus == 3:
            player.num_bombs += 1
            player.num_bonus = 0
        player.num_bonus = 0

        """проверка и удаление бомб"""
        for i in player.bomb_list:
            if i.time > 100:
                """удаление бомбы"""
                player.bomb_list.remove(i)
                all_sprite_list.remove(i)
                """появление взрыва"""
                expo = Explosion(i.rect.x, i.rect.y, 20, 20)
                all_sprite_list.add(expo)
                expo_list.add(expo)
                expo.break_list = break_list
                expo.wall_list = wall_list
                expo.player_list = all_players

                up, down, left, right, arr, play = expo.expo(player.expl_rad)
                print(up, down, left, right, arr)
                """убийство игрока"""
                for col in play:
                    for j in all_players:
                        if j.color == col:
                            j.is_alive = False
                            j.kill()
                """удаление блоков"""
                for j in arr:
                    for wall in all_sprite_list:
                        list = []
                        list.append(wall.rect.x)
                        list.append(wall.rect.y)

                        if list == j:
                            wall.kill()
                            """появлеине бонусов"""
                            rnd = random.uniform(0, 10)
                            if int(rnd) == 1:
                                rnd = random.uniform(1, 4)
                                bonus = Bonus(wall.rect.x, wall.rect.y)
                                bonus_list.add(bonus)
                                all_sprite_list.add(bonus)
                                if int(rnd) == 1:
                                    bonus.num_bonus = 1
                                    print("bonus1")
                                elif int(rnd) == 2:
                                    bonus.num_bonus = 2
                                    print("bonus2")
                                elif int(rnd) == 3:
                                    bonus.num_bonus = 3
                                    print("bonus 3")
                            else:
                                # print('нет бонусов')
                                pass

                """отрисовка взрывной волны"""
                for j in range(1, up + 1):
                    ver = Ver(expo.rect.x, expo.rect.y - j * 20)
                    expo.picture_list.add(ver)
                    all_sprite_list.add(ver)
                for j in range(1, down + 1):
                    ver = Ver(expo.rect.x, expo.rect.y + j * 20)
                    expo.picture_list.add(ver)
                    all_sprite_list.add(ver)
                for j in range(1, left + 1):
                    hor = Hor(expo.rect.x - j * 20, expo.rect.y)
                    expo.picture_list.add(hor)
                    all_sprite_list.add(hor)
                for j in range(1, right + 1):
                    hor = Hor(expo.rect.x + j * 20, expo.rect.y)
                    expo.picture_list.add(hor)
                    all_sprite_list.add(hor)

                player.num_of_bombs -= 1
            i.time += 1

        """направление движения для анимации"""
        if player.speed_x > 0:
            player.way = 'right'
        elif player.speed_x < 0:
            player.way = 'left'
        elif player.speed_y > 0:
            player.way = 'down'
        elif player.speed_y < 0:
            player.way = 'up'
        else:
            player.way = None

    """основной цикл событий"""
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                players[3].move(-players[3].speed, 0)
            elif e.key == pygame.K_RIGHT:
                players[3].move(players[3].speed, 0)
            elif e.key == pygame.K_UP:
                players[3].move(0, -players[3].speed)
            elif e.key == pygame.K_DOWN:
                players[3].move(0, players[3].speed)
            elif e.key == pygame.K_ESCAPE:
                done = True
            elif e.key == pygame.K_RSHIFT:
                """установка бомб"""
                if players[3].num_of_bombs < players[3].num_bombs and players[3].is_alive == True:
                    set_bomb(players[3])

            if e.key == pygame.K_a:
                players[0].move(-players[0].speed, 0)
            elif e.key == pygame.K_d:
                players[0].move(players[0].speed, 0)
            elif e.key == pygame.K_w:
                players[0].move(0, -players[0].speed)
            elif e.key == pygame.K_s:
                players[0].move(0, players[0].speed)
            elif e.key == pygame.K_ESCAPE:
                done = True
            elif e.key == pygame.K_TAB:
                """установка бомб"""
                if players[0].num_of_bombs < players[0].num_bombs and players[0].is_alive == True:
                    set_bomb(players[0])

            if e.key == pygame.K_j:
                players[1].move(-players[1].speed, 0)
            elif e.key == pygame.K_l:
                players[1].move(players[1].speed, 0)
            elif e.key == pygame.K_i:
                players[1].move(0, -players[1].speed)
            elif e.key == pygame.K_k:
                players[1].move(0, players[1].speed)
            elif e.key == pygame.K_ESCAPE:
                done = True
            elif e.key == pygame.K_SPACE:
                """установка бомб"""
                if players[1].num_of_bombs < players[1].num_bombs and players[1].is_alive == True:
                    set_bomb(players[1])

            if e.key == pygame.K_DELETE:
                players[2].move(-players[2].speed, 0)
            elif e.key == pygame.K_PAGEDOWN:
                players[2].move(players[2].speed, 0)
            elif e.key == pygame.K_HOME:
                players[2].move(0, -players[2].speed)
            elif e.key == pygame.K_END:
                players[2].move(0, players[2].speed)
            elif e.key == pygame.K_ESCAPE:
                done = True
            elif e.key == pygame.K_BACKSPACE:
                """установка бомб"""
                if players[2].num_of_bombs < players[2].num_bombs and players[2].is_alive == True:
                    set_bomb(players[2])

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                players[3].move(players[3].speed, 0)
            elif e.key == pygame.K_RIGHT:
                players[3].move(-players[3].speed, 0)
            elif e.key == pygame.K_UP:
                players[3].move(0, players[3].speed)
            elif e.key == pygame.K_DOWN:
                players[3].move(0, -players[3].speed)

            if e.key == pygame.K_a:
                players[0].move(players[0].speed, 0)
            elif e.key == pygame.K_d:
                players[0].move(-players[0].speed, 0)
            elif e.key == pygame.K_w:
                players[0].move(0, players[0].speed)
            elif e.key == pygame.K_s:
                players[0].move(0, -players[0].speed)

            if e.key == pygame.K_j:
                players[1].move(players[1].speed, 0)
            elif e.key == pygame.K_l:
                players[1].move(-players[1].speed, 0)
            elif e.key == pygame.K_i:
                players[1].move(0, players[1].speed)
            elif e.key == pygame.K_k:
                players[1].move(0, -players[1].speed)

            if e.key == pygame.K_DELETE:
                players[2].move(players[2].speed, 0)
            elif e.key == pygame.K_PAGEDOWN:
                players[2].move(-players[2].speed, 0)
            elif e.key == pygame.K_HOME:
                players[2].move(0, players[2].speed)
            elif e.key == pygame.K_END:
                players[2].move(0, -players[2].speed)

    """обновление всех обьектов"""
    all_sprite_list.update()

    """отрисовка всех обьектов"""
    all_sprite_list.draw(display)

    pygame.display.flip()
    clock.tick(FPS)
    # print(player.way)
if alive_players == 1:
    winner(players)

pygame.quit()
