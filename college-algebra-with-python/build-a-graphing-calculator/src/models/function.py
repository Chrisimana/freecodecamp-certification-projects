from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np
import sympy as sp
import math

@dataclass
class Function:
    # Class to represent a mathematical function
    expression: str
    color: str
    shading: str = "none"
    
    def __post_init__(self):
        self._function = None
        self._symbol = sp.symbols('x')
        
    def compile(self) -> Callable:
        # Compile expression into a callable function
        if self._function is None:
            try:
                # Replace ^ with ** for Python syntax
                expression_py = self.expression.replace('^', '**')
                # Create lambda function with safe namespace
                self._function = lambda x, f=expression_py: eval(
                    f, 
                    {'np': np, 'math': math, 'sp': sp, 'x': x}
                )
            except Exception as e:
                raise ValueError(f"Failed to compile function: {e}")
        return self._function
    
    def calculate(self, x: np.ndarray) -> np.ndarray:
        # Calculate function value for array x
        try:
            return self.compile()(x)
        except Exception as e:
            raise ValueError(f"Failed to calculate function: {e}")
    
    def to_sympy(self):
        # Convert to SymPy expression
        return sp.sympify(self.expression.replace('^', '**'))