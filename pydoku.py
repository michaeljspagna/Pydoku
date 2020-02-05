import random


class Pydoku(object):
    """Pydoku game logic along with board solver/generator backtracking algorithm"""

    VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self):
        """Initalized board to empty, win to false, and generates base game board"""
        self.win = False
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.answer = []
        self.generate_base()
        self.base = [row[:] for row in self.board]

    def __valid_col(self, col, val):
        """Checks if a value is valid in a given column"""
        for idx in range(9):
            if self.board[idx][col] == val:
                return False
        return True

    def __valid_row(self, row, val):
        """Checks if value is valid in a given row"""
        for idx in range(9):
            if self.board[row][idx] == val:
                return False
        return True

    def __valid_square(self, idx, val):
        """Checks if value is valid in a given latin square"""
        for i in range(idx[1] * 3, (idx[1] * 3) + 3):
            for j in range(idx[0] * 3, (idx[0] * 3) + 3):
                if self.board[i][j] == val and (i, j) != idx:
                    return False
        return True

    def check_valid(self, idx, val):
        """Checks if a value is valid at a (x,y) coordinate on the Pydoku board"""
        r = idx[1] // 3
        c = idx[0] // 3
        return (self.__valid_row(idx[0], val) and
                self.__valid_col(idx[1], val) and
                self.__valid_square((r, c), val))

    def __find_empty(self):
        """Finds the next empty (0 value) spot in the Pydoku board"""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def backtrack_fill(self, banned=-1):
        """Backtracking algorithm that generates a solved Pydoku board"""
        find = self.__find_empty()
        if not find:
            return True
        else:
            row, col = find
        values = self.VALUES[:]
        random.shuffle(values)
        for val in values:
            if banned == val:
                pass
            else:
                if self.check_valid((row, col), val):
                    self.board[row][col] = val

                    if self.backtrack_fill(banned):
                        return True

                    self.board[row][col] = 0
        return False

    def generate_base(self):
        """Extension of the backtracking algorithm that creates a Pydoku board with one possible outcome"""
        self.backtrack_fill()
        self.answer = [row[:] for row in self.board]
        back = [row[:] for row in self.board]
        rows = self.VALUES
        random.shuffle(rows)
        for r in rows:
            columns = self.VALUES
            random.shuffle(columns)
            removed = 0
            for c in columns:
                if removed == 7:
                    continue
                val = self.board[r - 1][c - 1]
                self.board[r - 1][c - 1] = 0
                if self.backtrack_fill(val):
                    back[r - 1][c - 1] = val
                else:
                    back[r - 1][c - 1] = 0
                    removed += 1
                self.board = [row[:] for row in back]

    def reset(self):
        """Resets the boards to a new base board"""
        self.win = False
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.generate_base()
        self.base = [row[:] for row in self.board]

    def solve(self):
        """Sets the board to the solution, and sets win = True"""
        self.board = self.answer
        self.win = True

    def insert(self, idx, val):
        """Checks if a value is legal to place in a given (x,y) coordinate, if so the value is added to the board"""
        if 0 <= val <= 9 and 0 <= idx[0] <= 9 and 0 <= idx[1] <= 9 and self.check_valid(idx, val):
            row, col = idx
            self.board[row][col] = val

    def check_win(self):
        """Checks for win condition, all rows, columns, and squares contain 1-9"""
        for row in range(9):
            if not self.__check_row(row):
                return False
        for col in range(9):
            if not self.__check_column(col):
                return False
        for row in range(3):
            for col in range(3):
                if not self.__check_square(row, col):
                    return False
        self.win = True
        return True

    def __check_vals(self, block):
        """Checks if a block contains 1-9"""
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        """Checks if a row contains 1-9"""
        return self.__check_vals(self.board[row])

    def __check_column(self, column):
        """Checks if a column contains 1-9"""
        return self.__check_vals([self.board[row][column] for row in range(9)])

    def __check_square(self, row, column):
        """Checks if a square contains 1-9"""
        return self.__check_vals(
            [
                self.board[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )

    def get_board(self):
        return self.board

    def get_answer(self):
        return self.answer

    def print_board(self):
        """Prints the board to the console"""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

