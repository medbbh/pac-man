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
level = boards
PI = math.pi
player_images = []
# RIGHT , LEFT , UP ,DOWN
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
startUp_count = 0
moving = False
num1 = (HEIGHT - 50) // 32
num2 = WIDTH // 30

player_x = 300
player_y = 425

direction = 0
counter = 0
flicker = False

powerUp = False
power_counter = 0
eaten_ghost = [False, False, False, False]
lives = 3

# Ghost var

#  blinky
red_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/red.png"), (30, 30)
)
# pinky
pink_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/pink.png"), (30, 30)
)
# inky
blue_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/blue.png"), (30, 30)
)
# clyde
orange_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/orange.png"), (30, 30)
)
# spooked
spooked_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/poweup.png"), (30, 30)
)
# dead
dead_img = pygame.transform.scale(
    pygame.image.load(f"assets/ghost_images/dead.png"), (30, 30)
)

red_x = 300
red_y = 200
red_direction = 0

pink_x = 300
pink_y = 200
pinky_direction = 2

blue_x = 300
blue_y = 200
blue_direction = 2

orange_x = 300
orange_y = 200
orange_direction = 2

targets = [
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
]

red_dead = False
pink_dead = False
blue_dead = False
orange_dead = False

red_box = False
pink_box = False
blue_box = False
orange_box = False

ghost_speed = 2
# # # # # # # # #


# class Ghost:



for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f"assets/player_images/{i}.png"), (30, 30)
        )
    )


def display_score():
    score_text = font.render(f"Score : {score}", True, "white")
    screen.blit(score_text, (10, 600))
    if not powerUp:
        pygame.draw.circle(screen, "red", (150, 608), 10)
    for i in range(lives):
        screen.blit(
            pygame.transform.scale(player_images[0], (20, 20)), (500 + i * 30, 595)
        )


def draw_board():
    # num1 = (HEIGHT - 50) // 32
    # num2 = WIDTH // 30

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
    if powerUp and power_counter < 600:
        power_counter += 1
    elif powerUp and power_counter >= 600:
        power_counter = 0
        powerUp = False
        eaten_ghost = [False, False, False, False]

    # set moving false for 3 sec
    if startUp_count < 180:
        moving = False
        startUp_count += 1
    else:
        moving = True

    screen.fill("black")
    draw_board()
    draw_player()
    display_score()
    center_x = player_x + 13
    center_y = player_y + 15
    turns_allowed = check_position(center_x, center_y)

    # not moving for 3 sec when the game start
    if moving:
        player_x, player_y = move_player(player_x, player_y)

    score, powerUp, power_counter, eaten_ghost = check_collisions(
        score, powerUp, power_counter, eaten_ghost
    )

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            elif event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            elif event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            elif event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    # for i in range(4):
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    # not working !!!!!!!!!!!!!
    # neyn yo5a8 men zer mevtou7 w yemreg men zer thani
    if player_x >= WIDTH - 30:
        player_x = 0
    elif player_x < -1:
        player_x = WIDTH - 30

    pygame.display.flip()
pygame.quit()
