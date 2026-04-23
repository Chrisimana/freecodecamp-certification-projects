import random
import tkinter as tk
from tkinter import ttk, messagebox

class GameAlgebra:
    def __init__(self, root):
        self.root = root
        self.difficulty_level = 1
        self.correct = 0
        self.attempted = 0
        self.streak = 0
        self.highest_streak = 0
        self.current_answer = None
        
        self.setup_gui()
        self.new_question()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="🧮 Algebra Practice", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.var_stats = tk.StringVar(value="Difficulty: Easy | Score: 0/0 | Streak: 0")
        ttk.Label(self.main_frame, textvariable=self.var_stats, 
                  font=('Arial', 10)).pack(pady=5)
        
        self.var_question = tk.StringVar(value="Click 'New Question' to start!")
        ttk.Label(self.main_frame, textvariable=self.var_question, 
                  font=('Arial', 14, 'bold'), background='white', 
                  relief='solid', padding=10).pack(pady=20)
        
        answer_frame = ttk.Frame(self.main_frame)
        answer_frame.pack(pady=10)
        
        ttk.Label(answer_frame, text="x =").pack(side='left')
        self.var_answer = tk.StringVar()
        entry = ttk.Entry(answer_frame, textvariable=self.var_answer, width=10, font=('Arial', 12))
        entry.pack(side='left', padx=5)
        entry.bind('<Return>', lambda e: self.check_answer())
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="New Question", command=self.new_question).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Check", command=self.check_answer).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Difficulty", command=self.change_difficulty).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_game).pack(side='left', padx=5)
        
        self.var_feedback = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.var_feedback, 
                  font=('Arial', 11), foreground='blue').pack(pady=10)

    def get_difficulty_name(self):
        return {1: "Easy", 2: "Medium", 3: "Hard"}[self.difficulty_level]

    def new_question(self):
        if random.choice([True, False]):
            equation, answer = self.create_one_step_question()
        else:
            equation, answer = self.create_two_step_question()
        
        self.current_answer = answer
        self.var_question.set(f"Solve for x:\n{equation}")
        self.var_answer.set("")
        self.var_feedback.set("")

    def create_one_step_question(self):
        if self.difficulty_level == 1:
            a = 1
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
        elif self.difficulty_level == 2:
            a = random.choice([1, -1, 2, -2])
            b = random.randint(-20, 20)
            c = random.randint(-20, 20)
        else:
            a = random.randint(-5, 5) or 1
            b = random.randint(-50, 50)
            c = random.randint(-50, 50)

        sign = "+" if b >= 0 else "-"
        equation = f"{'' if a==1 else '-' if a==-1 else a}x {sign} {abs(b)} = {c}"
        answer = round((c - b) / a, 2)
        return equation, answer

    def create_two_step_question(self):
        if self.difficulty_level == 1:
            a, c = random.randint(1, 5), random.randint(1, 5)
            b, d = random.randint(-10, 10), random.randint(-10, 10)
        elif self.difficulty_level == 2:
            a, c = random.randint(-5, 5), random.randint(-5, 5)
            b, d = random.randint(-20, 20), random.randint(-20, 20)
        else:
            a, c = random.randint(-10, 10), random.randint(-10, 10)
            b, d = random.randint(-50, 50), random.randint(-50, 50)

        while a == c:
            a = random.randint(-10, 10) or 1

        left = f"{'' if a==1 else '-' if a==-1 else a}x"
        left += f" + {b}" if b >= 0 else f" - {abs(b)}"
        right = f"{'' if c==1 else '-' if c==-1 else c}x"
        right += f" + {d}" if d >= 0 else f" - {abs(d)}"
        
        equation = f"{left} = {right}"
        answer = round((d - b) / (a - c), 2)
        return equation, answer

    def check_answer(self):
        if self.current_answer is None:
            messagebox.showwarning("Warning", "Create a question first!")
            return

        try:
            user_answer = float(self.var_answer.get())
            self.attempted += 1

            if abs(user_answer - self.current_answer) < 0.01:
                self.correct += 1
                self.streak += 1
                self.highest_streak = max(self.highest_streak, self.streak)
                message = f"✅ Correct! x = {self.current_answer}"
                if self.streak >= 3:
                    message += f"\n🔥 Streak {self.streak}!"
            else:
                self.streak = 0
                message = f"❌ Wrong. x = {self.current_answer}"

            self.var_feedback.set(message)
            self.update_stats()
            self.new_question()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def change_difficulty(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Difficulty")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Difficulty Level:", font=('Arial', 12)).pack(pady=20)
        
        var = tk.IntVar(value=self.difficulty_level)
        ttk.Radiobutton(dialog, text="Easy", variable=var, value=1).pack(pady=5)
        ttk.Radiobutton(dialog, text="Medium", variable=var, value=2).pack(pady=5)
        ttk.Radiobutton(dialog, text="Hard", variable=var, value=3).pack(pady=5)
        
        def apply():
            self.difficulty_level = var.get()
            self.update_stats()
            dialog.destroy()
            self.new_question()
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=20)

    def reset_game(self):
        self.correct = 0
        self.attempted = 0
        self.streak = 0
        self.highest_streak = 0
        self.update_stats()
        self.new_question()

    def update_stats(self):
        accuracy = (self.correct/self.attempted*100) if self.attempted > 0 else 0
        self.var_stats.set(
            f"Difficulty: {self.get_difficulty_name()} | "
            f"Score: {self.correct}/{self.attempted} | "
            f"Streak: {self.streak} | Accuracy: {accuracy:.1f}%"
        )