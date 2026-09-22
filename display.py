import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Scaling and Positioning")

s = 30
grid = [
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','S','.','.','#','.','.','.','.','.','#'],
    ['#','.','#','.','#','.','#','#','#','.','#'],
    ['#','.','#','.','.','.','#','G','#','.','#'],
    ['#','.','.','.','#','.','#','.','#','.','#'],
    ['#','#','#','.','#','.','.','.','#','.','#'],
    ['#','.','.','.','#','#','#','.','#','.','#'],
    ['#','.','#','.','.','X','.','.','#','.','#'],
    ['#','.','#','.','#','#','#','.','#','F','#'],
    ['#','X','.','.','.','.','X','.','.','.','#'],
    ['#','#','#','#','#','#','#','#','#','#','#']
]

tile_1 = pygame.image.load("tile_1.png").convert_alpha()
tile_1 = pygame.transform.scale(tile_1, (s, s))

tile_2 = pygame.image.load("tile_2.png").convert_alpha()
tile_2 = pygame.transform.scale(tile_2, (s, s))

tile_3 = pygame.image.load("tile_3.png").convert_alpha()
tile_3 = pygame.transform.scale(tile_3, (s, s))

tile_4 = pygame.image.load("tile_4.png").convert_alpha()
tile_4 = pygame.transform.scale(tile_4, (s, s))

bot = pygame.image.load("bot.png").convert_alpha()
bot = pygame.transform.scale(bot, (s, s))

bot_pos = [0, 100]
click_pos = (0, 0)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
text_surface = font.render("Hello, Pygame!", True, (0, 0, 0))

running = True
buu = True

while running:
    screen.fill((255, 255, 255))
    dt = clock.tick(60) / 1000
    speed = 100
    tl = random.randint(1, 4)

    for i in range(11):
        for j in range(11):
            if grid[i][j] == '.':
                screen.blit(tile_1, (j*s, i*s+100))
            elif grid[i][j] == '#':
                screen.blit(tile_2, (j*s, i*s+100))
            elif grid[i][j] == 'X':
                screen.blit(tile_3, (j*s, i*s+100))
            elif grid[i][j] == 'F':
                screen.blit(tile_4, (j*s, i*s+100))

    screen.blit(bot, bot_pos)
    screen.blit(text_surface, (10, 10))

    if buu:
        if math.floor(bot_pos[0]) < 200:
            text_surface = font.render("GO to 300 0", True, (0, 0, 0))
            bot_pos[0] += speed * dt
        elif math.floor(bot_pos[1]) < 400:
            text_surface = font.render("GO to 300 400", True, (0, 0, 0))
            bot_pos[1] += speed * dt
        else:
            buu = False
    else:
        if math.floor(bot_pos[0]) > 0:
            text_surface = font.render("GO to 0 400", True, (0, 0, 0))
            bot_pos[0] -= speed * dt
        elif math.floor(bot_pos[1]) > 100:
            text_surface = font.render("GO to 0 0", True, (0, 0, 0))
            bot_pos[1] -= speed * dt
        else:
            buu = True

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.image.save(screen, "screenshot.jpg")
                click_pos = event.pos
                print(f"Screen clicked at: {click_pos}")
                v = click_pos
                continue

pygame.quit()