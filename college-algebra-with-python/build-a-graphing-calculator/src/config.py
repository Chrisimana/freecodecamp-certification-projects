from dataclasses import dataclass

@dataclass
class Configuration:
    
    # Aesthetic colors
    PRIMARY_COLOR = "#2C3E50"      # Dark blue
    SECONDARY_COLOR = "#3498DB"    # Light blue
    ACCENT_COLOR = "#E74C3C"        # Red
    SUCCESS_COLOR = "#27AE60"       # Green
    BACKGROUND_COLOR = "#F8F9FA"        # White-gray
    TEXT_COLOR = "#2C3E50"         # Dark blue
    GRID_COLOR = "#ECF0F1"         # Light gray
    AXIS_COLOR = "#BDC3C7"       # Gray for axes
    
    # Fonts
    FONT_PRIMARY = ('Segoe UI', 10)
    FONT_TITLE = ('Segoe UI', 16, 'bold')
    FONT_SUB = ('Segoe UI', 12, 'bold')
    
    # Window size
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 900
    
    # Default plot limits
    X_MIN = -10
    X_MAX = 10
    Y_MIN = -10
    Y_MAX = 10
    
    # Function colors (gradient)
    FUNCTION_COLORS = [
        "#3498DB",  # Blue
        "#E74C3C",  # Red
        "#27AE60",  # Green
        "#F39C12",  # Orange
        "#9B59B6",  # Purple
        "#1ABC9C",  # Turquoise
    ]