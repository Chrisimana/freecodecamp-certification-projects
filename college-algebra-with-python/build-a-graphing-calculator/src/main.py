import tkinter as tk
from views.gui import GraphCalculatorGUI

def main():
    # Print banner
    print(""" Graph Calculator """)
    
    print("Usage Instructions:")
    print("• Enter function with variable x")
    print("• Use ** for exponent (example: x**2)")
    print("• Separate multiple functions with commas")
    print("• Shading: 'above', 'below', or 'none'")
    print("\nRunning application...\n")
    
    # Run the application
    root = tk.Tk()
    app = GraphCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()