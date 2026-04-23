import numpy as np
import colorsys

class VisualEffects:
    # Class for aesthetic visual effects
    
    @staticmethod
    def create_color_gradient(base_color: str, count: int) -> list:
        # Create color gradient from base color
        # Convert hex to RGB
        r = int(base_color[1:3], 16) / 255
        g = int(base_color[3:5], 16) / 255
        b = int(base_color[5:7], 16) / 255
        
        # Convert to HLS
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        # Create gradient
        colors = []
        for i in range(count):
            l_new = l + (i - count//2) * 0.1
            l_new = max(0.3, min(0.7, l_new))
            r_new, g_new, b_new = colorsys.hls_to_rgb(h, l_new, s)
            colors.append(f"#{int(r_new*255):02x}{int(g_new*255):02x}{int(b_new*255):02x}")
        
        return colors
    
    @staticmethod
    def create_aesthetic_plot(ax):
        # Create plot with aesthetic appearance
        ax.set_facecolor('#F8F9FA')
        ax.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
        
        # X and Y axes with glow effect
        ax.axhline(0, color='#2C3E50', linewidth=1.5, alpha=0.5)
        ax.axvline(0, color='#2C3E50', linewidth=1.5, alpha=0.5)
        
        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)