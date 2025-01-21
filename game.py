from files import *
from art import *

if __name__ == '__main__':
    game = FileExplorerGame()
    tprint("SnakeXplorer", font='small')
    print(SNAKE_ART)
    print('-'*60+'\n')
    print(INSTRUCTIONS.format(width=game.width))

    keyboard.wait('enter')
    game.play()

    tprint("Game Over", font='small')
    print("Score:", game.snake.length)
