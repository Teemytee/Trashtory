import pygame
import random
import time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_f,
    MOUSEBUTTONDOWN,
    K_LSHIFT
)  # импорты для того чтоб кнопки работали

# размер выводимого экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):  # класс Игрока
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("animations/character/sheet4l.png")  # Начальная картинка игрока, которая передается в сёрфейс
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(  # координаты появления игрока
                50,
                1000
            )
        )

    def update(self, pressed_keys):  # функция движения игрока
        if pressed_keys[K_UP]:  # для  кнопки *стрелка вверх*
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if pressed_keys[K_RIGHT] and pressed_keys[K_LSHIFT]:  # ускорение с помощью шифта
            self.rect.move_ip(15, 0)
        if pressed_keys[K_LEFT] and pressed_keys[K_LSHIFT]:  # ускорение с помощью шифта
            self.rect.move_ip(-15, 0)

        # Условия ограничения движения игрока за экран
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("animations/enemies/skelet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)  # ВАЖНО: чтобы пнгшка была чистой
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(0, 1)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Arrow(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("animations/weapon/knife.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self):
        self.rect.x += 15
        if self.rect.right - player.rect.x > 500:
            self.kill()



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

left = False
right = False
sright = False
sleft = False
strike = False
walkCount = 0
strikeCount = 0

walkRight = [pygame.image.load("animations/character/r0.png"),  # Анимации бега вправо
             pygame.image.load("animations/character/r1.png"),
             pygame.image.load("animations/character/r2.png"),
             pygame.image.load("animations/character/r3.png"),
             pygame.image.load("animations/character/r4.png"),
             pygame.image.load("animations/character/r5.png"), ]

walkLeft = [pygame.image.load("animations/character/l0.png"),  # Анимации бега влево
            pygame.image.load("animations/character/l1.png"),
            pygame.image.load("animations/character/l2.png"),
            pygame.image.load("animations/character/l3.png"),
            pygame.image.load("animations/character/l4.png"),
            pygame.image.load("animations/character/l5.png"), ]

attackList = [pygame.image.load("animations/character/attack0.png"),  # Анимации атаки
              pygame.image.load("animations/character/attack1.png"),
              pygame.image.load("animations/character/attack2.png"),
              pygame.image.load("animations/character/attack3.png"),
              pygame.image.load("animations/character/attack4.png"),
              pygame.image.load("animations/character/attack5.png"),
              pygame.image.load("animations/character/attack6.png"),
              pygame.image.load("animations/character/attack7.png"),
              pygame.image.load("animations/character/attack8.png"),
              pygame.image.load("animations/character/attack9.png"),
              pygame.image.load("animations/character/attack10.png")]

charr = pygame.image.load("animations/character/sheet4r.png") # Положение стоять вправо
charl = pygame.image.load("animations/character/sheet4l.png") # Положение стоять влево
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
arrows = pygame.sprite.Group()
score = 0
running = True

clock = pygame.time.Clock()


def redrawGameWindow():
    global walkCount, strikeCount
    screen.blit(bg, [0, 0])
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if walkCount + 1 >= 18:
        walkCount = 0
    if strikeCount >= 10:
        strikeCount = 0

    if left:
        walkCount += 1
        player.surf = walkLeft[walkCount // 3]
    elif right:
        player.surf = walkRight[walkCount // 3]
        walkCount += 1
    else:
        if sright:
            player.surf = charr
            walkCount = 0
        if sleft:
            player.surf = charl
            walkCount = 0
    if strike:
        clock.tick(24)
        strikeCount += 1
        player.surf = attackList[strikeCount]


bg = pygame.image.load("animations/background/background.png")

while running:
    clock.tick(24)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            strike = True
            arrow = Arrow()
            arrow.rect.x = player.rect.x
            arrow.rect.y = player.rect.y
            all_sprites.add(arrow)
            arrows.add(arrow)
        elif event.type == pygame.MOUSEBUTTONUP:
            strike = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_RIGHT:
                right = True
                left = False
            if event.key == K_LEFT:
                left = True
                right = False
        if event.type == pygame.KEYUP:
            if event.key == K_RIGHT and not pressed_keys[K_LEFT]:
                right = False
                left = False
                sright = True
                sleft = False
            if event.key == K_LEFT and not pressed_keys[K_RIGHT]:
                left = False
                right = False
                sright = False
                sleft = True
    for arrow in arrows:
        enemy_hit_list = pygame.sprite.spritecollide(arrow, enemies, True)
        for new_enemy in enemy_hit_list:
            arrows.remove(arrow)
            all_sprites.remove(arrow)
            score += 1
            print(score)
        if arrow.rect.y < -10:
            arrows.remove(arrow)
            all_sprites.remove(arrow)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    arrows.update()
    enemies.update()

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        print("Game over!")
        running = False
    redrawGameWindow()
    pygame.display.flip()


def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


print('Your score is: ', score)
