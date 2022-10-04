import pygame
from pygame import *


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    def __init__(self, x, y, color):
        # Call the parent's constructor
        super().__init__()

        self.go_left = [pygame.image.load(r"imagines/walking/" + color + "/left-1.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/left-2.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/left-3.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/left-2.png")]

        self.go_right = [pygame.image.load(r"imagines/walking/" + color + "/right-1.png"),
                         pygame.image.load(r"imagines/walking/" + color + "/right-2.png"),
                         pygame.image.load(r"imagines/walking/" + color + "/right-3.png"),
                         pygame.image.load(r"imagines/walking/" + color + "/right-2.png")]

        self.go_down = [pygame.image.load(r"imagines/walking/" + color + "/down-1.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/down-2.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/down-3.png"),
                        pygame.image.load(r"imagines/walking/" + color + "/down-2.png")]

        self.go_up = [pygame.image.load(r"imagines/walking/" + color + "/up-1.png"),
                      pygame.image.load(r"imagines/walking/" + color + "/up-2.png"),
                      pygame.image.load(r"imagines/walking/" + color + "/up-3.png"),
                      pygame.image.load(r"imagines/walking/" + color + "/up-2.png")]

        self.image = pygame.transform.scale(pygame.image.load(r"imagines/walking/" + color + "/down-2.png"), (16, 16))
        self.sprite = 0

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.speed_x = 0
        self.speed_y = 0

        self.walls = None
        self.break_list = None
        self.bomb_list = pygame.sprite.Group()
        self.bonus_list = pygame.sprite.Group()

        self.way = None
        self.num_of_bombs = 0
        self.is_alive = True
        self.color = color
        self.num_bonus = 0

        self.speed = 1.5
        self.expl_rad = 1
        self.num_bombs = 1

    def __del__(self):
        self.is_alive = False

    def move(self, hor, ver):
        """ Изменение скорости игрока """
        self.speed_x += hor
        self.speed_y += ver

    def update(self):
        """ Обновление положения игрока """

        if self.sprite + 1 >= 60:
            self.sprite = 0

        if self.way == 'left':
            self.image = pygame.transform.scale(self.go_left[self.sprite // 15], (16, 16))
            self.sprite += 1
        elif self.way == 'right':
            self.image = pygame.transform.scale(self.go_right[self.sprite // 15], (16, 16))
            self.sprite += 1
        elif self.way == 'up':
            self.image = pygame.transform.scale(self.go_up[self.sprite // 15], (16, 16))
            self.sprite += 1
        elif self.way == 'down':
            self.image = pygame.transform.scale(self.go_down[self.sprite // 15], (16, 16))
            self.sprite += 1
        else:
            self.image = pygame.transform.scale(pygame.image.load(r"imagines/walking/" + self.color + "/down-2.png"), (16, 16))

        # Move left/right
        self.rect.x += self.speed_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        break_hit_list = pygame.sprite.spritecollide(self, self.break_list, False)
        for block in (block_hit_list + break_hit_list):
            if self.speed_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.speed_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        break_hit_list = pygame.sprite.spritecollide(self, self.break_list, False)
        for block in (block_hit_list + break_hit_list):

            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        bonus_hit_list=pygame.sprite.spritecollide(self, self.bonus_list, False)
        for bon in bonus_hit_list:

            if bon.num_bonus == 3:
                self.num_bonus = 3
                bon.num_bonus = 0
            elif bon.num_bonus == 2:
                self.num_bonus = 2
                bon.num_bonus = 0
            elif bon.num_bonus == 1:
                self.num_bonus = 1
                bon.num_bonus = 0


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(r"imagines/unbreak-class.png"), (width, height))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Break(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(r"imagines/break-class.png"), (width, height))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(r"imagines/bomb.png"), (width, height))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.time = 0

        self.bomb_walls = None
        self.bomb_break = None


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r"imagines/explo/center/center-1.png"), (width, height))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.time = 27
        self.picture_list = pygame.sprite.Group()
        self.break_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.center = [pygame.image.load(r"imagines/explo/center/center-1.png"),
                       pygame.image.load(r"imagines/explo/center/center-2.png"),
                       pygame.image.load(r"imagines/explo/center/center-3.png"),
                       pygame.image.load(r"imagines/explo/center/center-4.png"),
                       pygame.image.load(r"imagines/explo/center/center-3.png"),
                       pygame.image.load(r"imagines/explo/center/center-2.png"),
                       pygame.image.load(r"imagines/explo/center/center-1.png")]

    def update(self):
            self.image = pygame.transform.scale(self.center[self.time // 4], (20, 20))

    """функция взрыва"""
    def expo(self, r):
        play = []
        ex = Explosion(self.rect.x - r * 20, self.rect.y - r * 20, r * 40 + 20, r * 40 + 20)
        # print(ex.rect)

        player_hit_list = pygame.sprite.spritecollide(ex, self.player_list, False)
        # for pl in player_hit_list:
        #     play.append(pl.color)

        """нахождение ближайшего неразрушаемого блока с каждой стороны"""
        block_hit_list = pygame.sprite.spritecollide(ex, self.wall_list, False)
        up = r
        down = r
        right = r
        left = r


        for wall in block_hit_list:
            for rad in range(1, r + 1):
                if self.rect.x + rad * 20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if rad - 1 < right:
                        right = rad - 1
                if self.rect.x - rad*20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if rad - 1 < left:
                        left = rad - 1
                if self.rect.y + rad*20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if rad - 1 < down:
                        down = rad - 1
                if self.rect.y - rad*20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if rad - 1 < up:
                        up = rad - 1

        """нахождение длинны необходимого взрыва в каждую сторону"""
        break_hit_list = pygame.sprite.spritecollide(ex, self.break_list, False)
        up1 = up
        down1 = down
        right1 = right
        left1 = left

        for wall in break_hit_list:
            for rad in range(1, right + 1):
                if self.rect.x + rad * 20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if rad - 1 < right1:
                        right1 = rad - 1
            for rad in range(1, left + 1):
                if self.rect.x - rad*20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if rad - 1 < left1:
                        left1 = rad - 1
            for rad in range(1, down + 1):
                if self.rect.y + rad*20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if rad - 1 < down1:
                        down1 = rad - 1
            for rad in range(1, up + 1):
                if self.rect.y - rad*20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if rad - 1 < up1:
                        up1 = rad - 1

        up2 = []
        down2 = []
        right2 = []
        left2 = []
        """нахождение координат блоков, которые надо сломать"""
        for rad in range(1, right + 1):
            for wall in break_hit_list:
                if self.rect.x + rad * 20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if len(right2) == 0:
                        right2.append([self.rect.x + 20 * rad, self.rect.y])

        for rad in range(1, left + 1):
            for wall in break_hit_list:
                if self.rect.x - rad * 20 == wall.rect.x and self.rect.y == wall.rect.y:
                    if len(left2) == 0:
                        left2.append([self.rect.x - 20 * rad, self.rect.y])

        for rad in range(1, down + 1):
            for wall in break_hit_list:
                if self.rect.y + rad * 20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if len(down2) == 0:
                        down2.append([self.rect.x, self.rect.y + 20 * rad])

        for rad in range(1, up + 1):
            for wall in break_hit_list:
                if self.rect.y - rad * 20 == wall.rect.y and self.rect.x == wall.rect.x:
                    if len(up2) == 0:
                        up2.append([self.rect.x, self.rect.y - 20 * rad])

        for pl in player_hit_list:
            x = ((pl.rect.x + 10) // 20) * 20
            y = ((pl.rect.y + 10) // 20) * 20
            if self.rect.x == x and self.rect.y == y:
                play.append(pl.color)
            for rad in range(1, right1 + 1):
                if self.rect.x + rad * 20 == x and self.rect.y == y:
                    play.append(pl.color)
            for rad in range(1, left1 + 1):
                if self.rect.x - rad*20 == x and self.rect.y == y:
                    play.append(pl.color)
            for rad in range(1, down1 + 1):
                if self.rect.y + rad*20 == y and self.rect.x == x:
                    play.append(pl.color)
            for rad in range(1, up1 + 1):
                if self.rect.y - rad*20 == y and self.rect.x == x:
                    play.append(pl.color)

        print('up', up)
        print('down', down)
        print('right', right)
        print('left', left)
        print('up1', up1)
        print('down1', down1)
        print('right1', right1)
        print('left1', left1)
        print('up2', up2)
        print('down2', down2)
        print('right2', right2)
        print('left2', left2)

        return up1, down1, left1, right1, list(up2 + down2 + left2 + right2), play
        # return 1, 2


class Hor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r"imagines/explo/horizontal/horiz-1.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.time = 27
        self.center = [pygame.image.load(r"imagines/explo/horizontal/horiz-1.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-2.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-3.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-4.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-3.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-2.png"),
                       pygame.image.load(r"imagines/explo/horizontal/horiz-1.png")]

    def update(self):
            self.image = pygame.transform.scale(self.center[self.time // 4], (20, 20))


class Ver(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r"imagines/explo/vertical/vert-1.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.time = 27
        self.center = [pygame.image.load(r"imagines/explo/vertical/vert-1.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-2.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-3.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-4.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-3.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-2.png"),
                       pygame.image.load(r"imagines/explo/vertical/vert-1.png")]

    def update(self):
        self.image = pygame.transform.scale(self.center[self.time // 4], (20, 20))


class Text:
    def __init__(self, text, font):
        self.font = pygame.font.Font("nasalization-rg.ttf", font)
        self.text = text

    def show(self, active, screen, pos):
        if active:
            colour = (255, 0, 0)
        else:
            colour = (255, 255, 255)
        textrect = self.font.render(self.text, True, colour).get_rect()
        screen.blit(self.font.render(self.text, 1, colour), pos)


class Bonus(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r"imagines/speed.png"), (20, 20))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        self.num_bonus=0

    def update(self):
        if self.num_bonus == 1:
            self.image = pygame.transform.scale(pygame.image.load(r"imagines/speed.png"), (20, 20))
        elif self.num_bonus == 2:
            self.image = pygame.transform.scale(pygame.image.load(r"imagines/wider.png"), (20, 20))
        elif self.num_bonus == 3:
            self.image = pygame.transform.scale(pygame.image.load(r"imagines/num_bomb.png"), (20, 20))

