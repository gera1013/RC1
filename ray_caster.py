import pygame

from math import cos, sin, pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (219, 127, 142)
WALLS = (32, 43, 88)
CHECKPOINT = (120, 104, 149)

class RayCaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.block_size = 50
        self.wall_height = 50

        self.step_size = 6

        self.set_color(WHITE)

        self.player = {
            "x" : 75,
            "y" : 55,
            "angle" : 90,
            "fov" : 60
        }

    def set_color(self, color):
        self.block_color = color

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_rect(self, x, y, color = WHITE):
        rect = (x, y, self.block_size, self.block_size)
        self.screen.fill(color, rect)

    def draw_player_icon(self, color = BLACK):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def cast_ray(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                return dist, self.map[j][i]

            self.screen.set_at((x,y), WHITE)

            dist += 1

    def render(self):

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        for x in range(0, half_width, self.block_size):
            for y in range(0, self.height, self.block_size):
                
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] != ' ':
                    self.draw_rect(x, y, WALLS if self.map[j][i] == '0' else CHECKPOINT)

        self.draw_player_icon()

        for i in range(half_width):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / half_width
            dist, c = self.cast_ray(angle)

            x = half_width + i 

            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180 )) * self.wall_height

            start = int(half_height - h / 2)
            end = int(half_height + h / 2)

            for y in range(start, end):
                self.screen.set_at((x, y), WALLS if c == '0' else CHECKPOINT)

        for i in range(self.height):
            self.screen.set_at((half_width, i), BLACK)
            self.screen.set_at((half_width + 1, i), BLACK)
            self.screen.set_at((half_width - 1, i), BLACK)


pygame.init()
screen = pygame.display.set_mode((1000, 500))

r = RayCaster(screen)

r.set_color((128, 0, 0))
r.load_map('./map.txt')

isRunning = True

move_forwards = False
move_backwards = False
move_left = False
move_right = False
turn_right = False
turn_left = False

while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                move_forwards = True
            elif ev.key == pygame.K_s:
                move_backwards = True
            elif ev.key == pygame.K_a:
                move_left = True
            elif ev.key == pygame.K_d:
                move_right = True
            elif ev.key == pygame.K_LEFT:
                turn_left = True
            elif ev.key == pygame.K_RIGHT:
                turn_right = True
        
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_w:
                move_forwards = False
            elif ev.key == pygame.K_s:
                move_backwards = False
            elif ev.key == pygame.K_a:
                move_left = False
            elif ev.key == pygame.K_d:
                move_right = False
            elif ev.key == pygame.K_LEFT:
                turn_left = False
            elif ev.key == pygame.K_RIGHT:
                turn_right = False

    if move_forwards:
        r.player['x'] += cos(r.player['angle'] * pi / 180) * r.step_size
        r.player['y'] += sin(r.player['angle'] * pi / 180) * r.step_size
    if move_backwards:
        r.player['x'] -= cos(r.player['angle'] * pi / 180) * r.step_size
        r.player['y'] -= sin(r.player['angle'] * pi / 180) * r.step_size
    if move_left:
        r.player['x'] -= cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        r.player['y'] -= sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if move_right:
        r.player['x'] += cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        r.player['y'] += sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if turn_left:
        r.player['angle'] -= 6
    if turn_right:
        r.player['angle'] += 6

    screen.fill(BACKGROUND)
    r.render()
    
    pygame.display.flip()

pygame.quit()
