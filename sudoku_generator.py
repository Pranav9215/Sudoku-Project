import math
import random


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):

        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        # Return the current state of the Sudoku board
        return self.board

    def print_board(self):
        # Print the current state of the Sudoku board to the console
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        # Check if the given number is not already present in the specified row
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        # Get a list of values in the specified column and check if the given number is not present in it
        values_in_col = []
        for row in self.board:
            values_in_col.append(row[col])
        return num not in values_in_col

    def valid_in_box(self, row_start, col_start, num):
        # Check if the given number is not present in the 3x3 box specified by the starting indices
        for i in range(self.box_length):
            for j in range(self.box_length):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        # Check if the given number is valid in the specified row, column, and box
        r = self.valid_in_row(row, num)
        c = self.valid_in_col(col, num)
        b = self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num)
        return (r and c and b)

    def fill_box(self, row_start, col_start):
        # Fill the 3x3 box with random values, ensuring each value occurs only once in the box
        box_values = random.sample(range(1, self.row_length + 1), self.row_length)
        index = 0
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = box_values[index]
                index += 1

    def fill_diagonal(self):
        # Fill the three boxes along the main diagonal of the Sudoku board
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        # (Provided function) Fills the remaining empty cells of the board
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        # Fill values in the Sudoku board by calling fill_diagonal and fill_remaining
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        # Removes a specified number of cells from the Sudoku board
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    return sudoku.get_board()


