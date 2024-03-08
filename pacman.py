import copy
import pygame
from board import boards
import math

pygame.init()

WIDTH = 600
HEIGHT = 650
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
level = copy.deepcopy(boards)
PI = math.pi
player_images = []

# RIGHT , LEFT , UP ,DOWN
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
startup_counter = 0
moving = False
num1 = (HEIGHT - 50) // 32
num2 = WIDTH // 30

player_x = 300
player_y = 425
direction = 0
blinky_x = 40
blinky_y = 35
blinky_direction = 0
pinky_x = 286
pinky_y = 247
pinky_direction = 2
inky_x = 286
inky_y = 270
inky_direction = 2
clyde_x = 286
clyde_y = 283
clyde_direction = 2

counter = 0
flicker = False

powerup = False
power_counter = 0
lives = 3
game_over = False
game_won = False
# Ghost var

#  blinky
blinky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/blinky.png"), (29, 29)
)
# pinky
pinky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/pinky.png"), (29, 29)
)
# inky
inky_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/inky.png"), (29, 29)
)
# clyde
clyde_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/clyde.png"), (29, 29)
)
# spooked
spooked_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/powerup.png"), (29, 29)
)
# dead
dead_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/dead.png"), (30, 30)
)



eaten_ghost = [False, False, False, False]

targets = [
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
]

blinky_dead = False
pinky_dead = False
inky_dead = False
clyde_dead = False

blinky_box = False
pinky_box = False
inky_box = False
clyde_box = False

ghost_speeds = [2, 2, 2, 2]
# # # # # # # # #


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 14
        self.center_y = self.y_pos + 14
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (
            eaten_ghost[self.id] and powerup and not self.dead
        ):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x, self.center_y), (30, 30))

        return ghost_rect

    def check_collisions(self):
        # RIGHT , LEFT , UP ,DOWN
        num3 = 11
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x - num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (
                level[self.center_y // num1][(self.center_x + num3) // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y + num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (
                level[(self.center_y - num3) // num1][self.center_x // num2] == 9
                and (self.in_box or self.dead)
            ):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 8 <= self.center_x % num2 <= 12:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 12:
                    if level[self.center_y // num1][
                        (self.center_x - num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num2) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num2) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 8 <= self.center_x % num2 <= 12:
                    if level[(self.center_y + num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y + num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][
                        self.center_x // num2
                    ] < 3 or (
                        level[(self.center_y - num3) // num1][self.center_x // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 12:
                    if level[self.center_y // num1][
                        (self.center_x - num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x - num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[1] = True
                    if level[self.center_y // num1][
                        (self.center_x + num3) // num2
                    ] < 3 or (
                        level[self.center_y // num1][(self.center_x + num3) // num2]
                        == 9
                        and (self.in_box or self.dead)
                    ):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 237 < self.x_pos < 365 and 249 < self.y_pos < 310:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -1:
            self.x_pos = WIDTH - 30
        elif self.x_pos > WIDTH - 30:
            self.x_pos = 0
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -1:
            self.x_pos = WIDTH - 30
        elif self.x_pos > WIDTH - 30:
            self.x_pos = 0
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -1:
            self.x_pos = WIDTH - 30
        elif self.x_pos > WIDTH - 30:
            self.x_pos = 0
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -1:
            self.x_pos = WIDTH - 30
        elif self.x_pos > WIDTH - 30:
            self.x_pos = 0
        return self.x_pos, self.y_pos, self.direction
    

for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f"assets/player_images/{i}.png"), (30, 30)
        )
    )

def draw_misc():
    # pygame.draw.circle(screen, "red", (365, 310), 1)

    score_text = font.render(f"Score : {score}", True, "white")
    screen.blit(score_text, (10, 600))
    if powerup:
        pygame.draw.circle(screen, "red", (150, 608), 10)
    for i in range(lives):
        screen.blit(
            pygame.transform.scale(player_images[0], (20, 20)), (500 + i * 30, 595)
        )
    if game_over:
        # pygame.draw(screen, "black", (50, 200, 400, 500), 0, 10)
        # pygame.draw(screen, "white", (70, 220, 360, 460), 0, 10)
        pygame.draw.rect(screen, "white", pygame.Rect(100, 200, 400, 200))
        pygame.draw.rect(screen, "gray", pygame.Rect(110, 210, 380, 180))
        gameover_text = font.render("Game over! press SPACE to restart!", True, "red")
        screen.blit(gameover_text, (120, 270))
    if game_won:
        pygame.draw.rect(screen, "white", pygame.Rect(100, 200, 400, 230))
        pygame.draw.rect(screen, "gray", pygame.Rect(110, 210, 380, 210))
        gameover_text = font.render(
            "YAYYY CONTGRATS! press SPACE to restart!", True, "green"
        )
        screen.blit(gameover_text, (120, 270))
    


def draw_board():

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(
                    screen,
                    "white",
                    (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),
                    4,
                )
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(
                    screen,
                    "red",
                    (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),
                    8,
                )
            if level[i][j] == 3:
                pygame.draw.line(
                    screen,
                    "blue",
                    (j * num2 + (0.5 * num2), i * num1),
                    (j * num2 + (0.5 * num2), i * num1 + num1),
                    3,
                )
            if level[i][j] == 4:
                pygame.draw.line(
                    screen,
                    "blue",
                    (j * num2, i * num1 + (0.5 * num1)),
                    (j * num2 + num2, i * num1 + (0.5 * num1)),
                    3,
                )
            if level[i][j] == 5:
                pygame.draw.arc(
                    screen,
                    "blue",
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 + (0.5 * num1)),
                        num2,
                        num1,
                    ],
                    0,
                    PI / 2,
                    3,
                )
            if level[i][j] == 6:
                pygame.draw.arc(
                    screen,
                    "blue",
                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                    PI / 2,
                    PI,
                    3,
                )
            if level[i][j] == 7:
                pygame.draw.arc(
                    screen,
                    "blue",
                    [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1],
                    PI,
                    3 * PI / 2,
                    3,
                )
            if level[i][j] == 8:
                pygame.draw.arc(
                    screen,
                    "blue",
                    [
                        (j * num2 - (num2 * 0.4)) - 2,
                        (i * num1 - (0.4 * num1)),
                        num2,
                        num1,
                    ],
                    3 * PI / 2,
                    2 * PI,
                    3,
                )
            if level[i][j] == 9:
                pygame.draw.line(
                    screen,
                    "white",
                    (j * num2, i * num1 + (0.5 * num1)),
                    (j * num2 + num2, i * num1 + (0.5 * num1)),
                    3,
                )


def draw_player():
    # 0 = right , 1 = left , 2 = up , 3 = down
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(
            pygame.transform.flip(player_images[counter // 5], True, False),
            (player_x, player_y),
        )
    elif direction == 2:
        screen.blit(
            pygame.transform.rotate(player_images[counter // 5], 90),
            (player_x, player_y),
        )
    elif direction == 3:
        screen.blit(
            pygame.transform.rotate(player_images[counter // 5], -90),
            (player_x, player_y),
        )


def check_position(centerx, centery):
    turns = [False, False, False, False]
    # num1 = (HEIGHT - 50) // 32
    # num2 = WIDTH // 30
    num3 = 11
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 8 <= centerx % num2 <= 12:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 12:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 8 <= centerx % num2 <= 12:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 12:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(playerx, playery):
    if direction == 0 and turns_allowed[0]:
        playerx += player_speed
    elif direction == 1 and turns_allowed[1]:
        playerx -= player_speed
    if direction == 2 and turns_allowed[2]:
        playery -= player_speed
    elif direction == 3 and turns_allowed[3]:
        playery += player_speed
    return playerx, playery


def check_collisions(game_score, power, power_count, eaten_ghosts):
    # num1 = (HEIGHT - 50) // 32
    # num2 = WIDTH // 30

    if 0 < player_x < 570:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            game_score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            game_score += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]

    return game_score, power, power_count, eaten_ghosts


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 300:
        runaway_x = 600
    else:
        runaway_x = 0
    if player_y < 300:
        runaway_y = 600
    else:
        runaway_y = 0
    return_target = (255, 265)

    print("1 : ",blinky.in_box)
    # 237 < self.x_pos < 365 and 249 < self.y_pos < 310:

    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 237 < blink_x < 365 and 249 < blink_y < 310:
                blink_target = (270, 50)
                
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 237 < ink_x < 365 and 249 < ink_y < 310:
                ink_target = (270, 50)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 237 < pink_x < 365 and 249 < pink_y < 310:
                pink_target = (270, 50)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (270, 50)
        elif not clyde.dead and eaten_ghost[3]:
            if 237 < clyd_x < 365 and 249 < clyd_y < 310:
                clyd_target = (270, 50)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 237 < blink_x < 365 and 249 < blink_y < 310:
                blink_target = (270, 50)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 237 < ink_x < 365 and 249 < ink_y < 310:
                ink_target = (270, 50)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 237 < pink_x < 365 and 249 < pink_y < 310:
                pink_target = (270, 50)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 237 < clyd_x < 365 and 249 < clyd_y < 310:
                clyd_target = (270, 50)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]


run = True

while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = True
    else:
        counter = 0
        flicker = False

    # Power Up instructions
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    # set moving false for 3 sec
    if startup_counter < 120 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill("black")
    draw_board()
    center_x = player_x + 15
    center_y = player_y + 15
    player_circle = pygame.draw.circle(screen, "black", (center_x, center_y), 12, 1)

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2

    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    draw_player()

    blinky = Ghost(
        blinky_x,
        blinky_y,
        targets[0],
        ghost_speeds[0],
        blinky_img,
        blinky_direction,
        blinky_dead,
        blinky_box,
        0,
    )
    inky = Ghost(
        inky_x,
        inky_y,
        targets[1],
        ghost_speeds[1],
        inky_img,
        inky_direction,
        inky_dead,
        inky_box,
        1,
    )
    pinky = Ghost(
        pinky_x,
        pinky_y,
        targets[2],
        ghost_speeds[2],
        pinky_img,
        pinky_direction,
        pinky_dead,
        pinky_box,
        2,
    )
    clyde = Ghost(
        clyde_x,
        clyde_y,
        targets[3],
        ghost_speeds[3],
        clyde_img,
        clyde_direction,
        clyde_dead,
        clyde_box,
        3,
    )
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
       
   

    center_x = player_x + 13
    center_y = player_y + 15
    turns_allowed = check_position(center_x, center_y)
    
    # not moving for 3 sec when the game start
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:

            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            print("#################")
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        print("33333333333333333333")
        
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if not powerup:
        if (
            (player_circle.colliderect(blinky.rect) and not blinky.dead)
            or (player_circle.colliderect(inky.rect) and not inky.dead)
            or (player_circle.colliderect(pinky.rect) and not pinky.dead)
            or (player_circle.colliderect(clyde.rect) and not clyde.dead)
        ):
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                blinky_x = 40
                blinky_y = 35
                blinky_direction = 0
                pinky_x = 286
                pinky_y = 247
                pinky_direction = 2
                inky_x = 286
                inky_y = 270
                inky_direction = 2
                clyde_x = 286
                clyde_y = 283
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if (
        powerup
        and player_circle.colliderect(blinky.rect)
        and eaten_ghost[0]
        and not blinky.dead
    ):
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            blinky_x = 40
            blinky_y = 35
            blinky_direction = 0
            pinky_x = 286
            pinky_y = 247
            pinky_direction = 2
            inky_x = 286
            inky_y = 270
            inky_direction = 2
            clyde_x = 286
            clyde_y = 283
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
    if (
        powerup
        and player_circle.colliderect(inky.rect)
        and eaten_ghost[1]
        and not inky.dead
    ):
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            blinky_x = 40
            blinky_y = 35
            blinky_direction = 0
            pinky_x = 286
            pinky_y = 247
            pinky_direction = 2
            inky_x = 286
            inky_y = 270
            inky_direction = 2
            clyde_x = 286
            clyde_y = 283
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if (
        powerup
        and player_circle.colliderect(pinky.rect)
        and eaten_ghost[2]
        and not pinky.dead
    ):
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            blinky_x = 40
            blinky_y = 35
            blinky_direction = 0
            pinky_x = 286
            pinky_y = 247
            pinky_direction = 2
            inky_x = 286
            inky_y = 270
            inky_direction = 2
            clyde_x = 286
            clyde_y = 283
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if (
        powerup
        and player_circle.colliderect(clyde.rect)
        and eaten_ghost[3]
        and not clyde.dead
    ):
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            blinky_x = 40
            blinky_y = 35
            blinky_direction = 0
            pinky_x = 286
            pinky_y = 247
            pinky_direction = 2
            inky_x = 286
            inky_y = 270
            inky_direction = 2
            clyde_x = 286
            clyde_y = 283
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if (
        powerup
        and player_circle.colliderect(blinky.rect)
        and not blinky.dead
        and not eaten_ghost[0]
    ):
        blinky_dead = True
        eaten_ghost[0] = True
        score += 2 ** eaten_ghost.count(True) * 100
    if (
        powerup
        and player_circle.colliderect(inky.rect)
        and not inky.dead
        and not eaten_ghost[1]
    ):
        inky_dead = True
        eaten_ghost[1] = True
        score += 2 ** eaten_ghost.count(True) * 100

    if (
        powerup
        and player_circle.colliderect(pinky.rect)
        and not pinky.dead
        and not eaten_ghost[2]
    ):
        pinky_dead = True
        eaten_ghost[2] = True
        score += 2 ** eaten_ghost.count(True) * 100

    if (
        powerup
        and player_circle.colliderect(clyde.rect)
        and not clyde.dead
        and not eaten_ghost[3]
    ):
        clyde_dead = True
        eaten_ghost[3] = True
        score += 2 ** eaten_ghost.count(True) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            elif event.key == pygame.K_LEFT:
                direction_command = 1
            elif event.key == pygame.K_UP:
                direction_command = 2
            elif event.key == pygame.K_DOWN:
                direction_command = 3
            elif event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 300
                player_y = 425
                direction = 0
                blinky_x = 40
                blinky_y = 35
                blinky_direction = 0
                pinky_x = 286
                pinky_y = 247
                pinky_direction = 2
                inky_x = 286
                inky_y = 270
                inky_direction = 2
                clyde_x = 286
                clyde_y = 283
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            elif event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            elif event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            elif event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    

    if player_x >= WIDTH - 30:
        player_x = 0
    elif player_x < -1:
        player_x = WIDTH - 30

    if blinky.in_box and blinky.dead:
        blinky_dead = False
    if inky.in_box and inky.dead:
        inky_dead = False
    if pinky.in_box and pinky.dead:
        pinky_dead = False
    if clyde.in_box and clyde.dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()
