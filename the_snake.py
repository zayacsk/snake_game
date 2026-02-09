from random import randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:

    def __init__(self, body_color=None) -> None:
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        raise NotImplementedError(
            f'Класс {type(self).__name__} не реализует метод draw()'
        )

    def draw_cell(self, position, body_color=None):
        body_color = body_color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)

        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):

    def __init__(self, occupied_cells=None, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(occupied_cells if occupied_cells else [])

    def randomize_position(self, occupied_cells):
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        self.draw_cell(self.position)


class Snake(GameObject):

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.last = None

    def update_direction(self, new_direction):
        if new_direction:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        self.positions.insert(
            0,
            ((head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
             (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT)
        )
        self.last = self.positions.pop()

    def draw(self):
        self.draw_cell(self.get_head_position())

        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        return self.positions[0]

    def eat(self):
        if self.last:
            self.positions.append(self.last)
            self.last = None


def handle_keys(snake):
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_ESCAPE):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            snake.update_direction(DIRECTIONS_MAP.get((snake.direction,
                                                      event.key)))


def main():
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.eat()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
