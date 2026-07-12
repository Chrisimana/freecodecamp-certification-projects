class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def get_area(self):
        return self.width * self.height
    
    def get_perimeter(self):
        return 2 * self.width + 2 * self.height
    
    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** 0.5
    
    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        
        picture = ""
        for _ in range(self.height):
            picture += "*" * self.width + "\n"
        return picture
    
    def get_amount_inside(self, shape):
        # Calculate how many times the given shape can fit horizontally and vertically
        horizontal_fit = self.width // shape.width
        vertical_fit = self.height // shape.height
        return horizontal_fit * vertical_fit
    
    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):
    def __init__(self, side):
        # Call parent constructor with same value for width and height
        super().__init__(side, side)
    
    def set_side(self, side):
        self.width = side
        self.height = side
    
    # Override set_width and set_height to maintain square properties
    def set_width(self, width):
        self.set_side(width)
    
    def set_height(self, height):
        self.set_side(height)
    
    def __str__(self):
        return f"Square(side={self.width})"


# Example usage
if __name__ == "__main__":
    # Create a rectangle object
    rect = Rectangle(10, 5)
    print(rect) 
    print(f"Area: {rect.get_area()}")  
    print(f"Perimeter: {rect.get_perimeter()}")
    print(f"Diagonal: {rect.get_diagonal()}")
    print(f"Picture:\n{rect.get_picture()}")
    
    # Create a square object
    sq = Square(5)
    print(sq) 
    print(f"Area: {sq.get_area()}")  
    print(f"Perimeter: {sq.get_perimeter()}") 
    print(f"Diagonal: {sq.get_diagonal()}") 
    
    # Test get_amount_inside method
    big_rect = Rectangle(30, 20)
    small_sq = Square(5)
    amount = big_rect.get_amount_inside(small_sq)
    print(f"Number of small squares that fit: {amount}")
    
    # Test picture size limit
    big_rect = Rectangle(60, 10)
    print(big_rect.get_picture())
