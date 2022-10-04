import pygame
from classes import Text


def about():
    done = False
    background = pygame.image.load(r"imagines/menu2.png")
    keys = pygame.image.load(r"imagines/keyboard.png")
    screen = pygame.display.get_surface()
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(background, (500, 500)), (0, 0))
        screen.blit(pygame.transform.scale(keys, (400, 200)), (50, 100))
        pygame.display.update()


def menu():
    pointer = 0
    display = pygame.display.set_mode((500, 500))
    screen = pygame.display.get_surface()
    background = pygame.image.load(r"imagines/menu2.png")
    done = False
    menu_items = [Text('Start', 32), Text('Control', 32), Text('Quit', 32)]
    bomberman = Text('BOMBERM4N', 46)
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 2
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    pointer = (pointer + 1) % 3
                elif e.key == pygame.K_UP:
                    pointer = (pointer - 1 + 3) % 3
                elif e.key == pygame.K_RETURN:
                    return pointer
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(background, (500, 500)), (0, 0))
        for i, j in zip(menu_items, [1, 2, 3]):
            i.show(j - 1 == pointer, screen, (100, j * 110))
        bomberman.show(False, screen, (10, 0))
        pygame.display.update()


def winner_finder(players):
    for player in players:
        if player.is_alive == 1:
            return player
    return players[0]


def winner(players):
    winner = winner_finder(players)
    pointer = 0
    display = pygame.display.set_mode((500, 500))
    screen = pygame.display.get_surface()
    background = pygame.image.load(r"imagines/menu2.png")
    done = False
    bomberman = Text('BOMBERM4N', 46)
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 2
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    pointer = (pointer + 1) % 3
                elif e.key == pygame.K_UP:
                    pointer = (pointer - 1 + 3) % 3
                elif e.key == pygame.K_RETURN:
                    return pointer
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(background, (500, 500)), (0, 0))
        screen.blit(pygame.transform.scale(winner.go_down[0], (100, 100)), (20, 170))
        Text(winner.color + " wins!", 32).show(0, screen, (120, 210))
        bomberman.show(False, screen, (10, 0))
        pygame.display.update()
