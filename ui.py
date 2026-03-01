import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import random
from config import CELL_SIZE, DELAY
from grid import Grid
from search import run_search

class App:
    def __init__(self, root):
        self.root = root
        self.rows = simpledialog.askinteger("Rows", "Enter rows:", minvalue=5, maxvalue=50)
        self.cols = simpledialog.askinteger("Cols", "Enter cols:", minvalue=5, maxvalue=50)

        self.canvas = tk.Canvas(root,
                                width=self.cols * CELL_SIZE,
                                height=self.rows * CELL_SIZE)
        self.canvas.pack()

        self.grid_obj = Grid(self.canvas, self.rows, self.cols)
        self.heuristic_type = "manhattan"
        self.algorithm = None

        self.create_buttons()
        self.canvas.bind("<Button-1>", self.on_click)
        self.grid_obj.draw()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Start", command=lambda: self.set_mode("start")).grid(row=0,column=0)
        tk.Button(frame, text="Goal", command=lambda: self.set_mode("goal")).grid(row=0,column=1)
        tk.Button(frame, text="Obstacle", command=lambda: self.set_mode("obstacle")).grid(row=0,column=2)
        tk.Button(frame, text="Random", command=self.random_maze).grid(row=0,column=3)

        tk.Button(frame, text="Run GBFS", command=lambda: self.run("gbfs")).grid(row=1,column=0)
        tk.Button(frame, text="Run A*", command=lambda: self.run("astar")).grid(row=1,column=1)

    def set_mode(self, mode):
        self.grid_obj.mode = mode

    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid_obj.toggle_cell(row, col)
            self.grid_obj.draw()

    def random_maze(self):
        density = simpledialog.askfloat("Density", "0-1:", minvalue=0, maxvalue=1)
        if density is None:
            return

        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_obj.grid[r][c] = 1 if random.random() < density else 0

        self.grid_obj.start = None
        self.grid_obj.goal = None
        self.grid_obj.draw()

    def run(self, algorithm):
        if not self.grid_obj.start or not self.grid_obj.goal:
            messagebox.showerror("Error", "Set Start & Goal")
            return

        start_time = time.time()

        came_from, cost, visited = run_search(
            self.grid_obj,
            self.heuristic_type,
            algorithm
        )

        end_time = int((time.time() - start_time)*1000)

        if came_from is None:
            messagebox.showinfo("Result", "No Path Found")
            return

        current = self.grid_obj.goal
        while current in came_from:
            current = came_from[current]
            if current != self.grid_obj.start:
                r, c = current
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1,y1,x2,y2,fill="green",outline="gray")

        messagebox.showinfo("Done", f"Cost: {cost} | Time: {end_time} ms")
