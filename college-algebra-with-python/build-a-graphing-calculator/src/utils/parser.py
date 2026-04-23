from typing import List, Tuple
from models.function import Function

class FunctionParser:
    # Class to parse function input
    
    @staticmethod
    def parse_function(input_str: str) -> List[str]:
        # Parse input string into function list
        if not input_str or not input_str.strip():
            return []
        return [f.strip() for f in input_str.split(',') if f.strip()]
    
    @staticmethod
    def parse_shading(input_str: str, function_count: int) -> List[str]:
        # Parse shading string
        if not input_str or not input_str.strip():
            return ["none"] * function_count
        
        shading = [a.strip().lower() for a in input_str.split(',')]
        # Normalize shading values
        shading = [
            "above" if a in ["above", "di atas", "atas"] else
            "below" if a in ["below", "di bawah", "bawah"] else
            "none"
            for a in shading
        ]
        
        # Adjust length to function count
        if len(shading) < function_count:
            shading.extend(["none"] * (function_count - len(shading)))
        elif len(shading) > function_count:
            shading = shading[:function_count]
            
        return shading