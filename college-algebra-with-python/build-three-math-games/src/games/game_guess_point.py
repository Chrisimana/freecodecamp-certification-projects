import matplotlib.pyplot as plt
import numpy as np
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GameGuessPoint:
    def __init__(self, root):
        self.root = root
        self.graph_size = 10
        self.num_points = 5
        self.points = []
        self.correct = 0
        self.attempted = 0
        
        self.setup_gui()
        self.setup_game()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="🎮 Guess the Point", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)
        
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Point #:").grid(row=0, column=0, padx=5)
        self.var_point = tk.StringVar(value="1")
        ttk.Spinbox(input_frame, from_=1, to=5, textvariable=self.var_point, width=5).grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="X:").grid(row=0, column=2, padx=5)
        self.var_x = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.var_x, width=8).grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Y:").grid(row=0, column=4, padx=5)
        self.var_y = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.var_y, width=8).grid(row=0, column=5, padx=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guess", command=self.guess).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Increase Difficulty", command=self.increase_difficulty).pack(side='left', padx=5)
        ttk.Button(button_frame, text="New Game", command=self.new_game).pack(side='left', padx=5)
        
        self.var_score = tk.StringVar(value="Score: 0/0 | Accuracy: 0%")
        ttk.Label(self.main_frame, textvariable=self.var_score, font=('Arial', 10, 'bold')).pack(pady=5)

    def setup_game(self):
        self.points = [(random.randint(-self.graph_size+1, self.graph_size-1),
                      random.randint(-self.graph_size+1, self.graph_size-1)) 
                     for _ in range(self.num_points)]
        self.display_plot()

    def display_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-self.graph_size, self.graph_size)
        self.ax.set_ylim(-self.graph_size, self.graph_size)
        self.ax.grid(True, alpha=0.3)
        
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]
        self.ax.scatter(x_vals, y_vals, color='red', s=100)
        
        for i, (x, y) in enumerate(self.points, 1):
            self.ax.text(x, y+0.5, str(i), fontsize=12, ha='center',
                        bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.7))
        
        self.canvas.draw()

    def guess(self):
        try:
            number = int(self.var_point.get())
            if number < 1 or number > self.num_points:
                messagebox.showwarning("Warning", "Invalid point number!")
                return

            guess_x = float(self.var_x.get())
            guess_y = float(self.var_y.get())
            
            if not self.var_x.get() or not self.var_y.get():
                messagebox.showwarning("Warning", "Enter X and Y coordinates!")
                return

            x_actual, y_actual = self.points[number-1]
            self.attempted += 1

            if abs(guess_x - x_actual) < 0.1 and abs(guess_y - y_actual) < 0.1:
                self.correct += 1
                messagebox.showinfo("Correct!", f"✅ ({x_actual}, {y_actual})")
            else:
                messagebox.showinfo("Incorrect", f"❌ Should be ({x_actual}, {y_actual})")

            self.update_score()
            self.var_x.set("")
            self.var_y.set("")

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers!")

    def increase_difficulty(self):
        self.graph_size += 5
        self.num_points = min(8, self.num_points + 1)
        self.setup_game()

    def new_game(self):
        self.correct = 0
        self.attempted = 0
        self.graph_size = 10
        self.num_points = 5
        self.setup_game()
        self.update_score()

    def update_score(self):
        accuracy = (self.correct/self.attempted*100) if self.attempted > 0 else 0
        self.var_score.set(f"Score: {self.correct}/{self.attempted} | Accuracy: {accuracy:.1f}%")