import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from config import Configuration
from controllers.calculator import CalculatorController
from utils.visual import VisualEffects
from utils.parser import FunctionParser
from views.styles import StyleManager

class GraphCalculatorGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Calculator")
        self.root.geometry(f"{Configuration.WINDOW_WIDTH}x{Configuration.WINDOW_HEIGHT}")
        self.root.configure(bg=Configuration.BACKGROUND_COLOR)
        
        # Initialize
        self.controller = CalculatorController()
        StyleManager.apply_style()
        
        # Setup UI
        self.setup_ui()
        
    # Build user interface
    def setup_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Card.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with gradient
        self.create_header(main_container)
        
        # Control panel
        control_panel = ttk.Frame(main_container)
        control_panel.pack(fill='x', pady=(0, 20))
        
        # Input section
        self.create_input_section(control_panel)
        
        # Button section
        self.create_button_section(control_panel)
        
        # Canvas for plot
        self.create_plot_canvas(main_container)
        
        # Console output
        self.create_console(main_container)

    # Create header with title
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="✦ Graph Calculator ✦",
            style='Title.TLabel'
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Mathematical Function Visualization with Aesthetics",
            style='Subtitle.TLabel'
        )
        subtitle.pack()
        
    # Create input section for functions
    def create_input_section(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Function Input", padding=15)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Function input
        ttk.Label(input_frame, text="Function:").grid(row=0, column=0, sticky='w', padx=5)
        self.function_entry = ttk.Entry(input_frame, width=60, font=('Consolas', 10))
        self.function_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.function_entry.bind('<Return>', lambda e: self.plot_function())
        
        # Shading input
        ttk.Label(input_frame, text="Shading:").grid(row=1, column=0, sticky='w', padx=5)
        self.shading_entry = ttk.Entry(input_frame, width=60, font=('Consolas', 10))
        self.shading_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.shading_entry.insert(0, "none")
        
        # Instructions
        hint = ttk.Label(
            input_frame,
            text="✏️ Example: x**2, sin(x), 2*x+3 | Separate with commas",
            foreground=Configuration.SECONDARY_COLOR
        )
        hint.grid(row=2, column=0, columnspan=2, pady=5)
        
        input_frame.columnconfigure(1, weight=1)

    # Create button section
    def create_button_section(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=10)
        
        # Action buttons
        buttons = [
            ("📊 Plot Graph", self.plot_function),
            ("📋 Create Table", self.create_table),
            ("🔄 Solve System", self.solve_system),
            ("📐 Solve Quadratic", self.solve_quadratic),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                style='Accent.TButton'
            )
            btn.grid(row=0, column=i, padx=5, sticky='ew')
            
        # Zoom controls
        zoom_frame = ttk.Frame(button_frame)
        zoom_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky='ew')
        
        ttk.Button(
            zoom_frame,
            text="🔍 Zoom In",
            command=lambda: self.zoom(0.5)
        ).pack(side='left', padx=5)
        
        ttk.Button(
            zoom_frame,
            text="🔎 Zoom Out",
            command=lambda: self.zoom(2)
        ).pack(side='left', padx=5)
        
        ttk.Button(
            zoom_frame,
            text="🔄 Reset View",
            command=self.reset_view
        ).pack(side='left', padx=5)
        
        button_frame.columnconfigure(tuple(range(4)), weight=1)

    # Create canvas for plot
    def create_plot_canvas(self, parent):
        canvas_frame = ttk.LabelFrame(parent, text="Function Visualization", padding=10)
        canvas_frame.pack(fill='both', expand=True, pady=10)
        
        # Create figure
        self.fig = Figure(figsize=(12, 6), facecolor='white', dpi=100)
        self.ax = self.fig.add_subplot(111)
        VisualEffects.create_aesthetic_plot(self.ax)
        
        # Set limits
        self.ax.set_xlim(self.controller.x_min, self.controller.x_max)
        self.ax.set_ylim(self.controller.y_min, self.controller.y_max)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    # Create console output
    def create_console(self, parent):
        console_frame = ttk.LabelFrame(parent, text="Output Console", padding=10)
        console_frame.pack(fill='x', pady=10)
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=8,
            font=('Consolas', 9),
            bg='white',
            fg=Configuration.TEXT_COLOR,
            wrap=tk.WORD
        )
        self.console.pack(fill='both', expand=True)
        
        # Tags for colors
        self.console.tag_config('error', foreground=Configuration.ACCENT_COLOR)
        self.console.tag_config('success', foreground=Configuration.SUCCESS_COLOR)
        self.console.tag_config('info', foreground=Configuration.SECONDARY_COLOR)

    # Function to log messages to console
    def log(self, message, message_type='info'):
        self.console.insert('end', message + '\n', message_type)
        self.console.see('end')
        self.root.update()

    # Function to clear console
    def clear_console(self):
        self.console.delete('1.0', 'end')

    # Function to plot input functions
    def plot_function(self):
        self.clear_console()
        self.ax.clear()
        VisualEffects.create_aesthetic_plot(self.ax)
        
        # Parse input
        function_str = self.function_entry.get()
        shading_str = self.shading_entry.get()
        
        if not function_str:
            messagebox.showwarning("Warning", "Enter at least one function")
            return
            
        # Parse functions
        function_list = FunctionParser.parse_function(function_str)
        shading_list = FunctionParser.parse_shading(shading_str, len(function_list))
        
        # Clear old functions
        self.controller.clear_all_functions()
        
        # Add new functions and plot
        x = np.linspace(self.controller.x_min, self.controller.x_max, 2000)
        
        for i, (expression, shading) in enumerate(zip(function_list, shading_list)):
            try:
                function = self.controller.add_function(expression, shading)
                y = function.calculate(x)
                
                # Plot with styling
                self.ax.plot(x, y, color=function.color, linewidth=2.5, label=expression)
                
                # Shading
                if shading == "above":
                    self.ax.fill_between(x, y, self.controller.y_max, 
                                        alpha=0.2, color=function.color)
                elif shading == "below":
                    self.ax.fill_between(x, y, self.controller.y_min,
                                        alpha=0.2, color=function.color)
                
                self.log(f"✓ {expression}", 'success')
                
            except Exception as e:
                self.log(f"✗ {expression}: {str(e)}", 'error')
        
        # Legend
        if self.controller.functions:
            self.ax.legend(frameon=True, fancybox=True, shadow=True, 
                          loc='best', fontsize=9)
        
        # Update limits
        self.ax.set_xlim(self.controller.x_min, self.controller.x_max)
        self.ax.set_ylim(self.controller.y_min, self.controller.y_max)
        
        self.canvas.draw()
        self.log("✨ Plotting complete!", 'success')

    # Create value table
    def create_table(self):
        if not self.controller.functions:
            messagebox.showwarning("Warning", "No function available")
            return
            
        self.clear_console()
        function = self.controller.functions[0]
        x_values = np.linspace(self.controller.x_min, self.controller.x_max, 15)
        
        self.log(f"📊 Value Table for {function.expression}", 'info')
        self.log("-" * 40)
        self.log(f"{'x':>8} | {'y':>10}")
        self.log("-" * 40)
        
        for x in x_values:
            try:
                y = function.calculate(x)
                self.log(f"{x:>8.2f} | {y:>10.2f}")
            except:
                self.log(f"{x:>8.2f} | {'error':>10}", 'error')

    # Solve system of equations
    def solve_system(self):
        try:
            intersection_points = self.controller.solve_system()
            
            self.clear_console()
            self.log("🔄 System Intersection Points:", 'info')
            
            if not intersection_points:
                self.log("No intersection points found", 'info')
            else:
                for x, y in intersection_points:
                    self.log(f"({x:.2f}, {y:.2f})")
                    # Plot point
                    self.ax.plot(x, y, 'o', color=Configuration.ACCENT_COLOR, 
                               markersize=10, markeredgecolor='white', 
                               markeredgewidth=2)
                    
                self.canvas.draw()
                self.log("✨ Intersection points marked", 'success')
                
        except Exception as e:
            self.log(f"Error: {str(e)}", 'error')

    # Solve quadratic equation
    def solve_quadratic(self):
        try:
            result = self.controller.solve_quadratic()
            
            self.clear_console()
            self.log("📐 Quadratic Function Analysis:", 'info')
            self.log(f"Form: {result['a']:.2f}x² + {result['b']:.2f}x + {result['c']:.2f}")
            self.log(f"Roots: {', '.join([f'{x:.2f}' for x in result['roots']])}")
            self.log(f"Vertex: ({result['vertex'][0]:.2f}, {result['vertex'][1]:.2f})")
            
            # Plot roots and vertex
            for x in result['roots']:
                self.ax.plot(x, 0, 'o', color=Configuration.SUCCESS_COLOR,
                           markersize=10, markeredgecolor='white', 
                           markeredgewidth=2, label='Root')
            
            x_vertex, y_vertex = result['vertex']
            self.ax.plot(x_vertex, y_vertex, 'o', color=Configuration.ACCENT_COLOR,
                       markersize=12, markeredgecolor='white', 
                       markeredgewidth=2, label='Vertex')
            
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"Error: {str(e)}", 'error')

    # Function to zoom in/out
    def zoom(self, factor):
        self.controller.zoom(factor)
        self.ax.set_xlim(self.controller.x_min, self.controller.x_max)
        self.ax.set_ylim(self.controller.y_min, self.controller.y_max)
        self.canvas.draw()
        self.log(f"{'🔍 Zoomed in' if factor < 1 else '🔎 Zoomed out'}", 'info')

    # Function to reset view
    def reset_view(self):
        self.controller.reset_view()
        self.ax.set_xlim(self.controller.x_min, self.controller.x_max)
        self.ax.set_ylim(self.controller.y_min, self.controller.y_max)
        self.canvas.draw()
        self.log("🔄 View reset", 'info')