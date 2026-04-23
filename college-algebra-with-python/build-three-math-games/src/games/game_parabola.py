import numpy as np
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GameParabola:
    def __init__(self, root):
        self.root = root
        self.level = 1
        self.max_height = 10
        self.wall_position = 0
        self.wall_height = 0
        self.score = 0
        self.attempts = 0
        
        self.setup_gui()
        self.new_level()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="🎯 Parabolic Motion", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.var_score = tk.StringVar(value="Score: 0 | Attempts: 0 | Accuracy: 0%")
        ttk.Label(self.main_frame, textvariable=self.var_score).pack(pady=5)
        
        level_frame = ttk.Frame(self.main_frame)
        level_frame.pack(pady=5)
        ttk.Label(level_frame, text="Mode:").pack(side='left')
        self.var_level = tk.IntVar(value=1)
        ttk.Radiobutton(level_frame, text="Slider", variable=self.var_level, 
                       value=1, command=self.on_level_change).pack(side='left', padx=10)
        ttk.Radiobutton(level_frame, text="Input", variable=self.var_level, 
                       value=2, command=self.on_level_change).pack(side='left', padx=10)
        
        self.slider_frame = ttk.Frame(self.main_frame)
        self.slider_a = tk.Scale(self.slider_frame, from_=-2, to=2, resolution=0.1,
                                orient='horizontal', label='a:', length=250)
        self.slider_a.pack(pady=2)
        self.slider_b = tk.Scale(self.slider_frame, from_=-5, to=5, resolution=0.1,
                                orient='horizontal', label='b:', length=250)
        self.slider_b.pack(pady=2)
        self.slider_c = tk.Scale(self.slider_frame, from_=0, to=10, resolution=0.1,
                                orient='horizontal', label='c:', length=250)
        self.slider_c.pack(pady=2)
        
        self.input_frame = ttk.Frame(self.main_frame)
        ttk.Label(self.input_frame, text="y = ax² + bx + c").pack()
        coeff_frame = ttk.Frame(self.input_frame)
        coeff_frame.pack(pady=5)
        
        ttk.Label(coeff_frame, text="a:").pack(side='left')
        self.var_a = tk.StringVar(value="0")
        ttk.Entry(coeff_frame, textvariable=self.var_a, width=6).pack(side='left', padx=2)
        
        ttk.Label(coeff_frame, text="b:").pack(side='left')
        self.var_b = tk.StringVar(value="0")
        ttk.Entry(coeff_frame, textvariable=self.var_b, width=6).pack(side='left', padx=2)
        
        ttk.Label(coeff_frame, text="c:").pack(side='left')
        self.var_c = tk.StringVar(value="0")
        ttk.Entry(coeff_frame, textvariable=self.var_c, width=6).pack(side='left', padx=2)
        
        self.slider_a.configure(command=self.update_plot)
        self.slider_b.configure(command=self.update_plot)
        self.slider_c.configure(command=self.update_plot)
        self.var_a.trace('w', lambda *_: self.update_plot())
        self.var_b.trace('w', lambda *_: self.update_plot())
        self.var_c.trace('w', lambda *_: self.update_plot())
        
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Check", command=self.check_solution).pack(side='left', padx=5)
        ttk.Button(button_frame, text="New Level", command=self.new_level).pack(side='left', padx=5)
        
        self.var_feedback = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.var_feedback, 
                  font=('Arial', 10), wraplength=600).pack(pady=5)
        
        self.slider_frame.pack()

    def on_level_change(self):
        if self.var_level.get() == 1:
            self.input_frame.pack_forget()
            self.slider_frame.pack()
        else:
            self.slider_frame.pack_forget()
            self.input_frame.pack()
        self.new_level()

    def new_level(self):
        self.wall_position = random.uniform(3, 7)
        self.wall_height = random.uniform(2, 8)
        
        if self.var_level.get() == 1:
            self.slider_a.set(random.uniform(-1, 1))
            self.slider_b.set(random.uniform(-2, 2))
            self.slider_c.set(random.uniform(0, 5))
        else:
            self.var_a.set("0")
            self.var_b.set("0")
            self.var_c.set("0")
        
        self.var_feedback.set(f"🎯 Wall at x={self.wall_position:.1f}, height={self.wall_height:.1f}")
        self.update_plot()

    def update_plot(self, event=None):
        self.ax.clear()
        
        try:
            if self.var_level.get() == 1:
                a, b, c = self.slider_a.get(), self.slider_b.get(), self.slider_c.get()
            else:
                a = float(self.var_a.get() or 0)
                b = float(self.var_b.get() or 0)
                c = float(self.var_c.get() or 0)
        except ValueError:
            a, b, c = 0, 0, 0
        
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, self.max_height)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Height')
        
        self.ax.axvline(x=self.wall_position, color='brown', linewidth=10, alpha=0.5)
        self.ax.axhline(y=self.wall_height, xmin=self.wall_position/10, 
                       xmax=self.wall_position/10, color='brown', linewidth=2, alpha=0.5)
        self.ax.text(self.wall_position, self.wall_height+0.5, 
                    f'Wall\n{self.wall_height:.1f}m', ha='center')
        
        x = np.linspace(0, 10, 200)
        y = a*x**2 + b*x + c
        
        mask = y >= 0
        if mask.any():
            self.ax.plot(x[mask], y[mask], 'b-', linewidth=2)
            
            y_wall = a*self.wall_position**2 + b*self.wall_position + c
            if y_wall >= 0:
                color = 'green' if y_wall > self.wall_height else 'red'
                self.ax.plot(self.wall_position, y_wall, 'o', color=color, markersize=8)
        
        self.canvas.draw()

    def check_solution(self):
        try:
            if self.var_level.get() == 1:
                a, b, c = self.slider_a.get(), self.slider_b.get(), self.slider_c.get()
            else:
                a = float(self.var_a.get() or 0)
                b = float(self.var_b.get() or 0)
                c = float(self.var_c.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return
        
        self.attempts += 1
        y_wall = a*self.wall_position**2 + b*self.wall_position + c
        
        if y_wall > self.wall_height:
            self.score += 1
            self.var_feedback.set(f"✅ SUCCESS! y={y_wall:.1f} > {self.wall_height:.1f}")
            self.new_level()
        else:
            difference = self.wall_height - y_wall
            self.var_feedback.set(f"❌ Failed! y={y_wall:.1f} < {self.wall_height:.1f} (short by {difference:.1f}m)")
        
        self.update_score()
        self.update_plot()

    def update_score(self):
        accuracy = (self.score/self.attempts*100) if self.attempts > 0 else 0
        self.var_score.set(f"Score: {self.score} | Attempts: {self.attempts} | Accuracy: {accuracy:.1f}%")