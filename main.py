import pygame
import os
import sys

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(self, filename='map_lvl.txt'):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 9, tile_height * pos_y + 3)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y

        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 9, tile_height * self.pos[1] + 3)
    #
    # def pos(self):


player = None

tile_images = {
    'wall': load_image('images/block.png'),
    'point': load_image('images/point.png'),
    'empty': load_image('images/background.png')
}
player_image = load_image('images/pacman.png')

tile_width = tile_height = 30

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player, lvl_x, lvl_y = generate_level(load_level('map_lvl.txt'))
running = True


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["PACMAN"]

    fon = pygame.transform.scale(load_image('images/fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


mapp = load_level('map_lvl.txt')
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            x, y = player.pos

            if event.key == pygame.K_LEFT:
                if x > 0 and mapp[y][x - 1] in ['.', '@']:
                    player.move(x - 1, y)

            if event.key == pygame.K_RIGHT:
                if x < (lvl_x - 1) and mapp[y][x + 1] in ['.', '@']:
                    player.move(x + 1, y)

            if event.key == pygame.K_UP:
                if y > 0 and mapp[x][y - 1] in ['.', '@']:
                    player.move(x, y - 1)

            if event.key == pygame.K_DOWN:
                if y < (lvl_y - 1) and mapp[x][y + 1] in ['.', '@']:
                    player.move(x, y + 1)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()