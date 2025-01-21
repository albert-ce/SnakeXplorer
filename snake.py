import numpy as np
import keyboard
import random
import time

def equal(d1, d2):
    return np.all(d1 == d2)

def not_equal(d1, d2):
    return not np.any(d1 == d2)

UP = np.array([-1,0])
RIGHT = np.array([0,1])
DOWN = np.array([1,0])
LEFT = np.array([0,-1])

BOARD = 0
SNAKE = 1
APPLE = 2

class SnakeSquare:
    def __init__(self, x=0, y=0, dir=RIGHT):
        self.pos = np.array([y,x])
        self.dir = dir
    
    def move(self, previous=None):
        self.pos += self.dir
        if previous:
            self.dir = previous.dir

class Snake:
    def __init__(self, x=0, y=0):
        self.body = [SnakeSquare(y, x)]
        self.head = self.body[0]
        self._dir = self.head.dir
        self.length = 1

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, new):
        self._dir = new
        self.head.dir = new

    def move(self):
        for current, previous in zip(reversed(self.body[1:]), reversed(self.body[:-1])):
            current.move(previous)
        self.head.move()

    def grow(self):
        y, x = self.body[-1].pos - self.body[-1].dir
        self.body.append(SnakeSquare(x, y, self.body[-1].dir))
        self.length += 1

class Game:
    def __init__(self, width=20, height=10, fps=5):
        self.fps = fps
        self.running = False
        self.width = width
        self.height = height
        self.board = np.full((height, width), BOARD)

        self.snake = Snake(height//2, width//2)
        self.apple = None
        self.new_apple()

        self.update_board()

        keyboard.on_press(self.get_input)

    def get_input(self, key):
        key_to_dir = {'w': UP, 'd': RIGHT, 's': DOWN, 'a': LEFT}

        if key.name in key_to_dir:
            dir = key_to_dir[key.name]
            if not_equal(self.snake.dir, -dir):
                self.snake.dir = dir
        elif key.name == 'esc':
            self.running = False

    def update_board(self):
        self.board[self.board != BOARD] = BOARD
        self.board[tuple(self.apple)] = APPLE
        for square in self.snake.body:
            y, x = square.pos
            if 0 <= y < self.height and 0 <= x < self.width:
                self.board[y, x] = SNAKE

    def new_apple(self):
        y, x = random.randint(0, self.height-1), random.randint(0, self.width-1)
        while any(np.all(np.array([y, x]) == square.pos) for square in self.snake.body):
            y, x = random.randint(0, self.height-1), random.randint(0, self.width-1)

        self.apple = np.array([y, x])

    def print_board(self):
        chars = np.full_like(self.board, '.', dtype='U8')
        chars[self.board == APPLE] = '*'
        chars[self.board == SNAKE] = '@'
        print("\033c")
        for row in chars:
            print(''.join(row))

    def check_collisions(self):
        y, x = self.snake.head.pos

        if x < 0 or x >= self.width or y < 0 or y >= self.height or self.board[y,x] == SNAKE:
            self.running = False
            self.ended = True

    def check_eating(self):
        if np.all(self.snake.head.pos == self.apple):
            self.snake.grow()
            self.new_apple()

    def update(self):
        if self.running:
            self.snake.move()
            self.check_collisions()
            if self.running:
                self.check_eating()
                self.update_board()

    def play(self):
        self.running = True
        while self.running:
            time.sleep(1/self.fps)
            self.update()
            self.print_board()
