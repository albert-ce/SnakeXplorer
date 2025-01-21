from files import *

if __name__ == '__main__':
    game = FileExplorerGame(10,8)
    print("Press Enter to Start")
    keyboard.wait('enter')
    game.play()
    