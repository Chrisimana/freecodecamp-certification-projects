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
        return 2 * (self.width + self.height)
    
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
    # Test Rectangle
    rect = Rectangle(10, 5)
    print(rect.get_area())  
    rect.set_height(3)
    print(rect.get_perimeter()) 
    print(rect) 
    print(rect.get_picture())

    # Test Square
    sq = Square(9)
    print(sq.get_area()) 
    sq.set_side(4)
    print(sq.get_diagonal())  
    print(sq)  
    print(sq.get_picture())

    # Test get_amount_inside
    rect.set_height(8)
    rect.set_width(16)
    print(rect.get_amount_inside(sq))  

    # Additional tests
    rect2 = Rectangle(15, 10)
    sq2 = Square(5)
    print(rect2.get_amount_inside(sq2))  

    rect3 = Rectangle(4, 8)
    rect4 = Rectangle(3, 6)
    print(rect3.get_amount_inside(rect4))  

    rect5 = Rectangle(2, 3)
    rect6 = Rectangle(3, 6)
    print(rect5.get_amount_inside(rect6))  