import tkinter as tk
from config import CELL_SIZE

class Grid:
    def __init__(self, canvas, rows, cols):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.goal = None
        self.mode = "obstacle"

    def draw(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "white"

                if self.grid[r][c] == 1:
                    color = "black"

                if self.start == (r, c):
                    color = "darkgreen"

                if self.goal == (r, c):
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="gray")

    def toggle_cell(self, row, col):
        if self.mode == "obstacle":
            if (row, col) != self.start and (row, col) != self.goal:
                self.grid[row][col] = 1 - self.grid[row][col]

        elif self.mode == "start":
            if self.grid[row][col] == 0:
                self.start = (row, col)

        elif self.mode == "goal":
            if self.grid[row][col] == 0:
                self.goal = (row, col)

    def clear(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.goal = None
