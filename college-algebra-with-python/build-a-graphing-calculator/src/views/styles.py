import tkinter as tk
from tkinter import ttk
from config import Configuration

class StyleManager:
    """Manager for GUI style"""
    
    @staticmethod
    def apply_style():
        """Apply custom style"""
        style = ttk.Style()
        
        # General style configuration
        style.theme_use('clam')
        
        # Button style
        style.configure(
            'Accent.TButton',
            background=Configuration.SECONDARY_COLOR,
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=Configuration.FONT_PRIMARY
        )
        style.map('Accent.TButton',
                  background=[('active', Configuration.PRIMARY_COLOR)])
        
        # Label style
        style.configure(
            'Title.TLabel',
            font=Configuration.FONT_TITLE,
            foreground=Configuration.PRIMARY_COLOR,
            background=Configuration.BACKGROUND_COLOR
        )
        
        style.configure(
            'Subtitle.TLabel',
            font=Configuration.FONT_SUB,
            foreground=Configuration.SECONDARY_COLOR,
            background=Configuration.BACKGROUND_COLOR
        )
        
        # Frame style
        style.configure(
            'Card.TFrame',
            background='white',
            relief='solid',
            borderwidth=1
        )
        
        return style