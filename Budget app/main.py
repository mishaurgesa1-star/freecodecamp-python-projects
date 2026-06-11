class Category:
    def __init__(self, name):
        # Store the category name (e.g. "Food", "Clothing")
        self.name = name
        # Every transaction (deposit/withdrawal) will be stored here as a dict
        self.ledger = []

    def deposit(self, amount, description=''):
        # description='' means it's optional — if not given, defaults to empty string 
        # We simply append a dict with the amount and description to the ledger
        self.ledger.append({'amount': amount, 'description': description})

    def get_balance(self):
        # Sum all 'amount' values in the ledger  
        # Withdrawals are stored as negative numbers, so they naturally reduce the balance  
        return sum(entry['amount'] for entry in self.ledger)

    def check_funds(self, amount):  
        # Returns True if we have enough balance, False if not
        # Used by both withdraw() and transfer() before making any changes
        return amount <= self.get_balance()           
                                                      
    def withdraw(self, amount, description=''):    
        # First check if we have enough funds — if not, do nothing and return False          
        if not self.check_funds(amount):
            return False  
        # Store as -amount (negative) so get_balance() subtracts it automatically   
        self.ledger.append({'amount': -amount, 'description': description}) 
        # Return True to signal the withdrawal was successful  
        return True  
                                     
    def transfer(self, amount, category): 
        # Check funds before doing anything
        if not self.check_funds(amount):
            return False
        # Withdraw from self with a description naming the destination
        self.withdraw(amount, f'Transfer to {category.name}')
        # Deposit into the other category with a description naming the source
        category.deposit(amount, f'Transfer from {self.name}')
        return True

    def __str__(self):
        # __str__ controls what happens when you print() this object

        # Center the category name in a 30-character string, filling gaps with '*'
        # e.g. "Food" becomes "*************Food*************"
        title = self.name.center(30, '*')

        rows = []
        for entry in self.ledger:
            # Truncate description to 23 characters max, then pad with spaces to fill 23 chars
            # ljust = left-justify (text on the left, spaces on the right)
            desc = entry['description'][:23].ljust(23)     
                                                                                      
            # Format amount to 2 decimal places, then right-align in 7 characters
            # rjust = right-justify (spaces on the left, number on the right)
            amt = f"{entry['amount']:.2f}".rjust(7)

            # Combine: 23 chars for description + 7 chars for amount = 30 chars per row
            rows.append(desc + amt)

        total = f"Total: {self.get_balance():.2f}"

        # Join title + all rows + total with newlines into one string
        return '\n'.join([title] + rows + [total])


def create_spend_chart(categories):
    # --- Step 1: Calculate total withdrawn per category ---
    withdrawals = [
        # Filter only negative entries (withdrawals), take absolute value, sum them
        sum(abs(e['amount']) for e in cat.ledger if e['amount'] < 0)
        for cat in categories
    ]

    # --- Step 2: Calculate each category's percentage of total spending ---
    total = sum(withdrawals)
    percentages = [
        # Multiply by 10, floor with int(), divide by 10 → rounds DOWN to nearest 10
        # e.g. 67.5% → int(6.75) * 10 = 60 (not 70)
        int((w / total) * 10) * 10 if total else 0
        for w in withdrawals
    ]

    # --- Step 3: Build the chart lines ---
    lines = ['Percentage spent by category']

    # Loop from 100 down to 0 in steps of 10 (one row per level)
    for level in range(100, -1, -10):
        # Right-align the level number in 3 chars, then add '| '
        # e.g. "100| ", " 90| ", "  0| "
        row = str(level).rjust(3) + '| '

        # For each category: place 'o' if its percentage reaches this level, else space
        # Each bar is followed by two spaces to separate bars
        row += ''.join('o  ' if pct >= level else '   ' for pct in percentages)
        lines.append(row)

    # --- Step 4: Horizontal dashes below the bars ---
    # 4 spaces for y-axis margin + dashes: 3 per category + 1 extra (extends past last bar)
    lines.append('    ' + '-' * (len(categories) * 3 + 1))

    # --- Step 5: Category names written vertically ---
    # Find the longest name so we know how many rows to print
    max_len = max(len(cat.name) for cat in categories)

    for i in range(max_len):
        # 5 spaces for the left margin (matching the chart above)
        row = '     '
        for cat in categories:
            # Pick the i-th character of the name, or a space if name is shorter
            letter = cat.name[i] if i < len(cat.name) else ' '
            # Each letter followed by two spaces (same spacing as bars above)
            row += letter + '  '
        lines.append(row)

    # Join all lines with newlines — no trailing newline at the end
    return '\n'.join(lines)


# ---- Example usage ----
if __name__ == '__main__':
    food = Category('Food')
    food.deposit(1000, 'initial deposit')
    food.withdraw(10.15, 'groceries')
    food.withdraw(15.89, 'restaurant and more food for dessert')

    clothing = Category('Clothing')
    food.transfer(50, clothing)

    auto = Category('Auto')
    auto.deposit(500, 'auto budget')
    auto.withdraw(150, 'oil change')

    print(food)
    print()
    print(create_spend_chart([food, clothing, auto]))
