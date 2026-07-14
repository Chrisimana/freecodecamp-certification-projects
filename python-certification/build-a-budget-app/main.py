class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        # Title line
        title = self.name.center(30, "*")
        
        # Ledger items
        items = ""
        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:.2f}"
            items += f"{description:<23}{amount:>7}\n"
        
        # Total
        total = f"Total: {self.get_balance():.2f}"
        
        return f"{title}\n{items}{total}"


def create_spend_chart(categories):
    # Calculate total withdrawals for each category
    withdrawals = []
    for category in categories:
        total_withdrawn = 0
        for item in category.ledger:
            if item["amount"] < 0:
                total_withdrawn += -item["amount"]
        withdrawals.append(total_withdrawn)
    
    # Calculate percentages
    total_spent = sum(withdrawals)
    if total_spent > 0:
        percentages = [(withdrawal / total_spent) * 100 for withdrawal in withdrawals]
    else:
        percentages = [0] * len(categories)
    
    # Round down to nearest 10
    rounded_percentages = [int(p // 10) * 10 for p in percentages]
    
    # Build the chart
    chart = "Percentage spent by category\n"
    
    # Y-axis and bars 
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for p in rounded_percentages:
            if p >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"
    
    # Horizontal line
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    # Category names vertically
    max_length = 0
    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)
    
    for i in range(max_length):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        if i < max_length - 1:
            chart += "\n"
    
    return chart


# Create test_settings dictionary
test_settings = {
    'theme': 'light',
    'language': 'english',
    'notifications': 'enabled'
}


# Example usage
if __name__ == "__main__":
    # Create categories
    food = Category("Food")
    clothing = Category("Clothing")
    entertainment = Category("Entertainment")
    
    # Make transactions
    food.deposit(1000, "deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food")
    food.transfer(50, clothing)
    
    clothing.deposit(500, "deposit")
    clothing.withdraw(25.55, "shoes")
    
    entertainment.deposit(1000, "deposit")
    entertainment.withdraw(125, "concert tickets")
    
    # Print each category
    print(food)
    print()
    print(clothing)
    print()
    print(entertainment)
    print()
    
    # Print spending chart
    print(create_spend_chart([food, clothing, entertainment]))