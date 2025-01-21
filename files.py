from snake import *
from PIL import Image
import os

class FileExplorerGame(Game):
    def __init__(self, width=10, height=8, fps=2, file_size=(50,50)):
        super().__init__(width, height, fps)
        self.SNAKE_IMG = Image.new("RGB", file_size, (29, 182, 83))
        self.BOARD_IMG = Image.new("RGB", file_size, (255, 255, 255))
        self.APPLE_IMG = Image.new("RGB", file_size, (220, 67, 52))

        self.indexs = np.arange(width*height).reshape(height, width)
        self.prev_board = self.board.copy()
        self.diff = np.zeros_like(self.board, dtype=bool)

        self.delete_all()
        for (y, x), val in np.ndenumerate(self.board):
            index = y*width+x
            self.save_img(index, val)

    def delete_all(self):
        try:
            dir = os.path.join(".", "game")
            for file in os.listdir(dir):
                file_path = os.path.join(dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error: {e}")

    def save_img(self, index, val):
        if val == BOARD:
            self.BOARD_IMG.save(os.path.join('game', f"{index}.png"), "PNG")
        elif val == SNAKE:
            self.SNAKE_IMG.save(os.path.join('game', f"{index}.png"), "PNG")
        elif val == APPLE:
            self.APPLE_IMG.save(os.path.join('game', f"{index}.png"), "PNG")

    def update_board(self):
        self.prev_board = self.board.copy()
        super().update_board()
        self.diff = self.prev_board != self.board

    def save_board(self):
        for i in self.indexs[self.diff]:
            y, x = np.unravel_index(i, self.board.shape)
            self.save_img(i, self.board[y, x])

    def play(self):
        self.running = True
        while self.running:
            time.sleep(1/self.fps)
            self.update()
            self.save_board()
            keyboard.press('f5')
        self.delete_all()
