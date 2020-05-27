from constants import BLACK, WHITE, FLOOR, BOMB_SIZE, SCREEN_LENGTH, CAR_LENGTH, CAR_HEIGHT
import pygame

pygame.init()


class Button(pygame.sprite.Sprite):
    down = False

    def __init__(self, color, text, size, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size[0], size[1]))
        self.rect = self.image.get_rect(center=center)

        self.color = [color[0], color[1], color[2]]
        self.text = text
        self.size = size

        self.image.fill(self.color)
        pygame.draw.rect(self.image, BLACK, (-3, -3, self.size[0] + 3, self.size[1] + 3), 3)
        self.image.blit(self.text.image, self.text.rect)

    def button_down(self):
        if not self.down:
            self.down = True

            for i in range(3):
                self.color[i] = self.color[i] * .9

            self.image.fill(self.color)
            pygame.draw.rect(self.image, BLACK, (0, 0, self.size[0] + 3, self.size[1] + 3), 3)
            self.image.blit(self.text.image, self.text.rect)

    def button_up(self):
        if self.down:
            self.down = False

            for i in range(3):
                self.color[i] = self.color[i] / .9

            self.image.fill(self.color)
            pygame.draw.rect(self.image, BLACK, (-3, -3, self.size[0] + 3, self.size[1] + 3), 3)
            self.image.blit(self.text.image, self.text.rect)


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, center, font=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect(center=center)


class Bomb(pygame.sprite.Sprite):
    speed = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bomb.png')
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, collide):
        if not collide:
            self.rect.y += round(self.speed)
            self.speed += .04

        if self.rect.y >= FLOOR - BOMB_SIZE:
            self.kill()


class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/car.png')
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_LENGTH - CAR_LENGTH) / 2
        self.rect.y = FLOOR - CAR_HEIGHT
