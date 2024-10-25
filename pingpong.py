import pygame
import sys
import random

pygame.init()

# Получаем размеры экрана
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создаем окно в полноэкранном режиме
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Ping Pong Game')

clock = pygame.time.Clock()

# Свойства ракеток
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Свойства мяча
BALL_SIZE = 10
BALL_SPEED_X = 3 * random.choice((1, -1))
BALL_SPEED_Y = 3 * random.choice((1, -1))

# Ракетка игрока (левая)
player_paddle = pygame.Rect(
    50,
    SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Ракетка компьютера (правая)
ai_paddle = pygame.Rect(
    SCREEN_WIDTH - 50 - PADDLE_WIDTH,
    SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# Мяч
ball = pygame.Rect(
    SCREEN_WIDTH // 2 - BALL_SIZE // 2,
    SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
    BALL_SIZE,
    BALL_SIZE
)

# Инициализация джойстика
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("Геймпад не подключен")
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Управление с геймпада
    if joystick.get_init():
        axis_y = joystick.get_axis(1)  # Вертикальная ось левого стика
        player_paddle.y += int(axis_y * PADDLE_SPEED * 2)

        # Ограничение ракетки внутри экрана
        if player_paddle.top < 0:
            player_paddle.top = 0
        if player_paddle.bottom > SCREEN_HEIGHT:
            player_paddle.bottom = SCREEN_HEIGHT
    else:
        print("Геймпад не инициализирован")
        running = False
        break

    # Движение ракетки компьютера (простой ИИ)
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += PADDLE_SPEED
    else:
        ai_paddle.y -= PADDLE_SPEED

    # Ограничение ракетки компьютера
    if ai_paddle.top < 0:
        ai_paddle.top = 0
    if ai_paddle.bottom > SCREEN_HEIGHT:
        ai_paddle.bottom = SCREEN_HEIGHT

    # Движение мяча
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Отскок от верхней и нижней границы
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1

    # Отскок от ракеток
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        BALL_SPEED_X *= -1

    # Счет (сброс мяча)
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        BALL_SPEED_X = 3 * random.choice((1, -1))
        BALL_SPEED_Y = 3 * random.choice((1, -1))

    # Очистка экрана
    screen.fill(BLACK)

    # Рисуем ракетки и мяч
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Рисуем сетку
    pygame.draw.aaline(
        screen,
        WHITE,
        (SCREEN_WIDTH // 2, 0),
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT)
    )

    # Обновляем экран
    pygame.display.flip()

    # Частота кадров
    clock.tick(60)

pygame.quit()
sys.exit()
