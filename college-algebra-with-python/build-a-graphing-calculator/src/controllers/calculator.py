import numpy as np
import sympy as sp
from typing import List, Tuple, Optional
from models.function import Function
from utils.parser import FunctionParser
from config import Configuration

class CalculatorController:
    # Controller to manage calculator operations
    
    def __init__(self):
        self.functions: List[Function] = []
        self.x_min = Configuration.X_MIN
        self.x_max = Configuration.X_MAX
        self.y_min = Configuration.Y_MIN
        self.y_max = Configuration.Y_MAX
        
    def add_function(self, expression: str, shading: str = "none") -> Optional[Function]:
        # Add new function
        try:
            function = Function(expression, Configuration.FUNCTION_COLORS[len(self.functions) % len(Configuration.FUNCTION_COLORS)], shading)
            function.compile()  # Test compile
            self.functions.append(function)
            return function
        except Exception as e:
            raise ValueError(f"Failed to add function: {e}")
    
    def clear_all_functions(self):
        # Clear all functions
        self.functions.clear()
    
    def solve_system(self, index1: int = 0, index2: int = 1) -> List[Tuple[float, float]]:
        # Solve system of two equations
        if len(self.functions) < 2:
            raise ValueError("Need at least 2 functions")
        
        f1 = self.functions[index1]
        f2 = self.functions[index2]
        
        x = sp.symbols('x')
        expr1 = f1.to_sympy()
        expr2 = f2.to_sympy()
        
        solution = sp.solve(expr1 - expr2, x)
        intersection_points = []
        
        for sol in solution:
            try:
                x_val = float(sol.evalf())
                y_val = float(f1.calculate(x_val))
                intersection_points.append((x_val, y_val))
            except:
                continue
                
        return intersection_points
    
    def solve_quadratic(self, index: int = 0) -> dict:
        # Solve quadratic equation
        if not self.functions:
            raise ValueError("No function available")
        
        f = self.functions[index]
        expr = f.to_sympy()
        x = sp.symbols('x')
        
        # Check degree
        degree = sp.degree(expr, x)
        if degree != 2:
            raise ValueError("Function is not quadratic")
        
        # Solution
        solution = sp.solve(expr, x)
        roots = []
        for sol in solution:
            try:
                roots.append(float(sol.evalf()))
            except:
                continue
        
        # Vertex
        a = float(expr.coeff(x**2))
        b = float(expr.coeff(x))
        c = float(expr.coeff(x, 0))
        
        vertex_x = -b/(2*a)
        vertex_y = float(expr.subs(x, vertex_x))
        
        return {
            'roots': roots,
            'vertex': (vertex_x, vertex_y),
            'a': a,
            'b': b,
            'c': c
        }
    
    def zoom(self, factor: float):
        # Zoom in/out
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        self.x_min += x_range * (1 - 1/factor) / 2
        self.x_max -= x_range * (1 - 1/factor) / 2
        self.y_min += y_range * (1 - 1/factor) / 2
        self.y_max -= y_range * (1 - 1/factor) / 2
    
    def reset_view(self):
        # Reset to default view
        self.x_min = Configuration.X_MIN
        self.x_max = Configuration.X_MAX
        self.y_min = Configuration.Y_MIN
        self.y_max = Configuration.Y_MAX