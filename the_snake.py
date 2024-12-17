from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет интерфейса
INTR_COLOR = (51, 255, 153)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Основной классс для игровых объектов"""

    def __init__(self):
        """Инициализация"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Функция рисования объекта, заглушка для будущих экземпляров"""
        pass


class Apple(GameObject):
    """Экземляр класса GameObject, описывает объект яблоко"""

    def __init__(self):
        """Инициализация"""
        super().__init__()
        self.randomize_position(self.position)
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_pos):
        """Определяем рандомную позицию яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        # Проверка, чтобы яблоко не спавнилось на змейке.
        while self.position in snake_pos:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Рисуем яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Экземляр класса GameObject, описывает объект змейка"""

    def __init__(self):
        """Инициализация"""
        super().__init__()
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Управляем направлением джвижения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змйеки"""
        x_head_pos, y_head_pos = self.get_head_position()
        new_pos = ((x_head_pos + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                   (y_head_pos + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
                   )

        self.positions.insert(0, new_pos)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисуем голову и тело змейки"""
        for position in self.positions[0:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Определяем позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    # Инициализируем pygame, создаем экземпляры классов, нач. скорость игры 20.
    pygame.init()
    apple = Apple()
    snake = Snake()

    # Стартовая скорость, счётчик яблок, рекорд по яблокам.
    game_speed = 20
    eat_apples = 0
    record = 0

    # Шрифт для интерфейса.
    font = pygame.font.Font(None, 25)

    # Игровые звуки.
    sound_eat = pygame.mixer.Sound('game_res\\eat_sound.wav')
    sound_lose = pygame.mixer.Sound('game_res\\lose.wav')

    while True:
        clock.tick(game_speed)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Кушаем яблоко. Увеличиваем длину и счетчик яблок на 1.
        # Скаждым скушаным яблоком скорость растет на 0.5.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            eat_apples += 1
            game_speed += 0.5
            apple.randomize_position(snake.positions)
            sound_eat.play()
            # Проверяем условие смены рекорда.
            # Если текщий счетчик яблок больше рекорда, то меняем рекорд.
            if record < eat_apples:
                record += 1
        # Проверяем столкновение змейки с самой собой.
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            game_speed = 20
            eat_apples = 0
            apple.randomize_position(snake.positions)
            sound_lose.play()

        # Рисуем фон, яблоко и змейку.
        background = pygame.image.load('game_res\\background.jpg')
        screen.blit(background, (0, 0))
        apple.draw()
        snake.draw()

        # Рисуем интерфейс.
        text_snake_l = font.render(
            f'Текущая длина: {snake.length}', True, INTR_COLOR)
        text_eat_a = font.render(
            f'Съедено яблок: {eat_apples}', True, INTR_COLOR)
        text_record = font.render(
            f'Макс. яблок: {record}', True, INTR_COLOR)
        text_now_speed = font.render(
            f'Скорость: {game_speed}', True, INTR_COLOR)
        screen.blit(text_snake_l, (5, 5))
        screen.blit(text_eat_a, (5, 25))
        screen.blit(text_record, (500, 5))
        screen.blit(text_now_speed, (500, 25))
        pygame.display.update()


if __name__ == '__main__':
    main()
