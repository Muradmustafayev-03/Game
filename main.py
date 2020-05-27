import pygame
from random import randint
from sprites import Button, Text, Car, Bomb
from constants import GREEN, WHITE, RED, GRAY, LIGHT_BLUE, SCREEN_LENGTH, SCREEN_WIDTH, BUTTON_SIZE, FLOOR, BOMB_SIZE, \
    CAR_SPEED, CAR_LENGTH, LAND_WIDTH, BLACK

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 500)

display = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))
pygame.display.set_caption('It\'s a simple python game')

clock = pygame.time.Clock()
FPS = 60

car = Car()

bombs = pygame.sprite.Group()
bombs_number = 0

score = bombs_number - len(bombs)
results = [0]

level = 1
timer = 0

play_text = Text('PLAY', 80, RED, (BUTTON_SIZE[0] / 2, BUTTON_SIZE[1] / 2))
play_button = Button(GREEN, play_text, BUTTON_SIZE, (SCREEN_LENGTH / 2, 150))

menu_text = Text('MENU', 80, RED, (BUTTON_SIZE[0] / 2, BUTTON_SIZE[1] / 2))
menu_button = Button(GREEN, menu_text, BUTTON_SIZE, (SCREEN_LENGTH / 2, 300))

game_over_text = Text('GAME OVER', 100, RED, (SCREEN_LENGTH / 2, 50))


def menu():
    record = max(results)
    results.clear()
    results.append(record)
    record_text = Text('Record:' + str(record), 80, RED, (SCREEN_LENGTH / 2, 300))

    display.fill(WHITE)
    display.blit(play_button.image, play_button.rect)
    display.blit(record_text.image, record_text.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.rect.x <= event.pos[0] <= play_button.rect.x + BUTTON_SIZE[0] and \
                    play_button.rect.y <= event.pos[1] <= play_button.rect.y + BUTTON_SIZE[1]:
                play_button.button_down()

        elif event.type == pygame.MOUSEBUTTONUP:
            if play_button.down:
                play_button.button_up()

                while not pygame.sprite.spritecollideany(car, bombs):
                    play()

                while True:
                    game_over()

    clock.tick(FPS)
    pygame.display.update()


def play():
    global bombs_number
    global score
    global level
    global timer

    score = bombs_number - len(bombs)

    level_text = Text('Level:' + str(level), 30, BLACK, (0, 0))
    score_text = Text('Score:' + str(score), 30, BLACK, (0, 0))
    level_text.rect.x = score_text.rect.x = 10
    level_text.rect.y = 20
    score_text.rect.y = 50

    land = pygame.Surface((SCREEN_LENGTH, LAND_WIDTH))
    land.fill(GRAY)
    land.blit(level_text.image, level_text.rect)
    land.blit(score_text.image, score_text.rect)

    display.fill(LIGHT_BLUE)
    display.blit(land, (0, FLOOR))
    display.blit(car.image, car.rect)

    bombs.draw(display)
    bombs.update(pygame.sprite.spritecollideany(car, bombs))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.USEREVENT:
            timer += 1
            for i in range(1, level + 1):
                bombs.add(Bomb(randint(0, SCREEN_LENGTH - BOMB_SIZE), -randint(BOMB_SIZE, BOMB_SIZE * level)))
                bombs_number += 1

    if timer == 40:
        level += 1
        timer = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        car.rect.x += CAR_SPEED

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        car.rect.x -= CAR_SPEED

    if car.rect.x > SCREEN_LENGTH - CAR_LENGTH:
        car.rect.x = SCREEN_LENGTH - CAR_LENGTH

    if car.rect.x < 0:
        car.rect.x = 0

    clock.tick(FPS)


def game_over():
    global level
    global bombs_number
    global timer

    timer = 0
    level = 1
    bombs_number = 0
    results.append(score)
    score_text = Text('Score:' + str(score), 80, RED, (SCREEN_LENGTH / 2, 150))

    display.fill(WHITE)
    display.blit(menu_button.image, menu_button.rect)
    display.blit(score_text.image, score_text.rect)
    display.blit(game_over_text.image, game_over_text.rect)

    for bomb in bombs:
        bomb.kill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_button.rect.x <= event.pos[0] <= menu_button.rect.x + BUTTON_SIZE[0] and \
                    menu_button.rect.y <= event.pos[1] <= menu_button.rect.y + BUTTON_SIZE[1]:
                menu_button.button_down()

        elif event.type == pygame.MOUSEBUTTONUP:
            if menu_button.down:
                menu_button.button_up()

                while True:
                    menu()

    pygame.display.update()
    clock.tick(FPS)


while True:
    menu()
