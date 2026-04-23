import tkinter as tk
from tkinter import ttk
from games.game_guess_point import GameGuessPoint
from games.game_algebra import GameAlgebra
from games.game_parabola import GameParabola

class ThreeGameApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Three Math Games")
        self.root.geometry("900x830")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(self.root)
        
        self.frame_point = ttk.Frame(self.notebook)
        self.frame_algebra = ttk.Frame(self.notebook)
        self.frame_parabola = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_point, text="🎯 Guess the Point")
        self.notebook.add(self.frame_algebra, text="🧮 Algebra")
        self.notebook.add(self.frame_parabola, text="🎯 Parabola")
        
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.game_point = GameGuessPoint(self.frame_point)
        self.game_algebra = GameAlgebra(self.frame_algebra)
        self.game_parabola = GameParabola(self.frame_parabola)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThreeGameApplication()
    app.run()