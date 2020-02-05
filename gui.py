#!/usr/bin/env python3
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from pydoku import Pydoku
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class GUI(Frame):
    """
    GUI, Draws board and makes use of the game logic
    """

    def __init__(self, parent, pydoku):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pydoku = pydoku
        self.row, self.col = -1, -1
        self.__init_gui()
        self.original = [row[:] for row in self.pydoku.board]

    def __init_gui(self):
        """Initializes the tkinter gui"""
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="Clear answers", command=self.__clear_answers)
        solve_button = Button(self, text="Solve Game", command=self.__solve)
        clear_button.pack(side=BOTTOM)
        solve_button.pack(side=BOTTOM)
        self.__draw_grid()
        self.__draw_puzzle()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """Draws the grid on the gui"""
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        """Adds the values to the gui"""
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                val = self.pydoku.board[i][j]
                if val != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    color = "sea green" if val == self.pydoku.base[i][j] else "black"
                    self.canvas.create_text(
                        x, y, text=val, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )
            if self.pydoku.check_win():
                self.__draw_victory()

    def __cell_clicked(self, event):
        """Selects cell when clicked"""
        if self.pydoku.win:
            return
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.pydoku.board[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        """Attempts to enter value when key is clicked. Only accepts 1-9"""
        if self.pydoku.win:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.pydoku.insert((self.row, self.col), int(event.char))
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.pydoku.check_win():
                self.__clear_answers()

    def __clear_answers(self):
        """Clear and resets board"""
        self.pydoku = Pydoku()
        self.__draw_puzzle()
        self.__draw_cursor()

    def __solve(self):
        """Puts the solved board in the gui"""
        self.pydoku.solve()
        self.__draw_puzzle()
        self.__draw_cursor()


if __name__ == '__main__':
    game = Pydoku()
    root = Tk()
    GUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()
