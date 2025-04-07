class Product: # create class, object and attribute
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        else:
            print(f"Not enough stock for {self.name}.")
            return False

    def restock(self,quantity):
        self.stock += quantity

    def is_low_stock(self):
        return self.stock < 5

    def display(self):
        print(f"{self.name:<10} ${self.price:<10.2f} {self.stock:<10}")

class ShoppingCart: # Dictionary to store items in cart with the product's details and quantity
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product.update_stock(quantity):
            if product.name in self.items:
                self.items[product.name]['quantity'] += quantity
            else:
                self.items[product.name] = {'product': product, 'quantity': quantity}

    def remove_item(self, product, quantity):
        if not self.items:
            print("There are no items in your cart.")
            return
        if product.name in self.items:
            if quantity > self.items[product.name]['quantity']:
                print(f"you only have {self.items[product.name]['quantity']} of {product.name} in your cart.")
            else:
                self.items[product.name]['quantity'] -= quantity
                product.restock(quantity)
                if self.items[product.name]['quantity'] == 0:
                    del self.items[product.name]
                print(f"{quantity} x {product.name} removed from cart.")
        else:
                print(f"{product.name} is not in your cart.")

    def view_cart(self):
        if not self.items:
            print("Your Cart is empty.")
            return
        print("\n===== Shopping Cart =====")
        for item, details in self.items.items():
            total_price = details['product'].price * details['quantity']
            print(f"{item}: {details['quantity']} x ${details['product'].price:.2f} = ${total_price:.2f}")
        print("-" * 40)
        total = sum(details['product'].price * details['quantity'] for details in self.items.values())
        print(f"Subtotal: ${total:.2f}")

    def calculate_total(self):
        subtotal = sum(details['product'].price * details['quantity'] for details in self.items.values())
        tax = subtotal * 0.10
        discount = 0
        if subtotal > 5000:
            discount = subtotal * 0.05
        total = subtotal + tax - discount
        return subtotal, tax, discount, total

    def clear_cart(self):
        self.items.clear()
import time

class POS:
    def __init__(self):
        self.products = {
            'Milk': Product('1. Milk', 300, 15),
            'Salt': Product('2. Salt', 120, 15),
            'Eggs': Product('3. Eggs', 30, 12),
            'Broom': Product('4.Broom', 1200, 18),
            'Fork': Product('5. Fork',80, 15),
            'Spoon': Product('6. Spoon',80, 25),
            'Knife': Product('7. Knife',90, 30),
            'Red Wine': Product('8. Red Wine', 4300, 10),
            'Orange Juice': Product('9. Orange Juice', 280.78, 20),
            'Disinfectant': Product('10. Disinfectant', 320, 25),
            'Ray & Nephew Rum': Product('11. Ray & Nephew Rum', 1500, 20),
        }
        self.cart = ShoppingCart()
    def display_products(self):
        print("\nAvailable Products:")
        print("{:<10} {:<10} {:<10}". format("Product", "Price ($)", "Stock"))
        print("-" * 30)
        for product in self.products.values():
            product.display()

    def add_to_cart(self):
        while True:
            self.display_products()
            try:
                product_num = int(input("\nEnter product number you wish to add to cart:")) -1
                if product_num == -1:
                    print("Returning to the main menu.")
                    break
                if 0 <= product_num < len(self.products):
                    product = list(self.products.values())[product_num]
                else:
                    print("Invalid option, please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter corresponding number")
                continue
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be grater than zero")
                continue
            if product.stock >= quantity:
                self.cart.add_item(product, quantity)
                print(f"{quantity} x {product.name} was added to your cart.")
                if product.stock <=5:
                    print(f"===Warning===: {product.name} Stock is low(Amount remaining: {product.stock}) ")
            else:
                print("Not enough stock, please try again.")
            continue_choice = input("Do you wish to add another product to your cart? (y/n): ").lower()
            if continue_choice != 'y':
                print("Returning to the main menu...")
                break # this allows the program to exit the loop.

    def remove_from_cart(self):
        self.display_products()
        try:
            product_num = int(input("\nEnter product number to remove product from your cart:")) -1
            if 0 <= product_num <len(self.products):
                product = list(self.products.values())[product_num]
                quantity = int(input(f"Enter quantity to remove: "))
                self.cart.remove_item(product, quantity)
            else:
                print("Invalid product number, please try again.")
        except ValueError:
            print("Invalid input, please try the corresponding number to the item you wish to remove from your cart.")

    def checkout(self):
        if not self.cart.items:
            print("\nCart is empty. Cannot proceed to checkout.")
            return
        subtotal, tax, discount, total = self.cart.calculate_total()
        print("\n===== CHECKOUT =====")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (10%) : ${tax: .2f}")
        if discount > 0:
            print(f"Discount (5%): -${discount:.2f}")
        print(f"Total: ${total:.2f}")

        while True:
            try:
                payment = float(input("Enter payment amount: $"))
            except ValueError:
                print("Invalid input. Please enter a valid figure.")
                continue
            if payment >= total:
                change = payment - total
                print(f"Change: ${change:.2f}")
                self.generate_receipt(subtotal, tax, discount, total, payment, change)
                self.cart.clear_cart()
                break
            else:
                print(f"Insufficient payment. A Total: of ${total:.2f} is required.")
                alternate = input("Do you wish to (1), remove an item from your cart or (2) enter another amount? (Please enter 1 or 2):")
                if alternate == '1':
                    self.remove_from_cart() #calls the function so the customer can decide what item to remove in order to reduce the total.
                    subtotal, tax, discount, total = self.cart.calculate_total()
                    print(f"\nUpdated total: ${total:.2f}") # Displays the new total after item(s) have been removed.
                elif alternate == '2':
                    continue # facilitate the cashier entering another amount
                else:
                    print("Invalid option, please select 1 or 2.")
                    continue
    def generate_receipt(self, subtotal, tax, discount, total, payment, change):
        print("\n=========== RECEIPT ===========")
        print("BEST BUY RETAIL STORE")
        print("14b Alexandra Crescent, St Andrew")
        print("Tel 876-432-3451")
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print("---------------------------------")
        for name, info in self.cart.items.items():
            total_price = info['product'].price * info['quantity']
            print(f"{name:<10} x{info['quantity']} @ ${info['product'].price:.2f} = ${total_price:.2f}")
            print("---------------------------")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (10%): ${tax:.2f}")
        if discount > 0:
            print(f"Discount (5%): -${discount:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Payment:${payment:.2f}")
        print(f"Change: ${change:.2f}")
        print("Thank you for Shopping With Us!")
        print("===========================")

    def low_stock_alert(self):
                print("\nLow Stock Alert:")
                for product in self.products.values():
                    if product.is_low_stock():
                        print(f"{product.name} - Stock: {product.stock}")

    def run(self):
        while True:
            print("\n========================================================")
            print("\n Welcome to BEST BUY RETAIL STORE POS SYSTEM")
            print("\n========================================================")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Low Stock Alert")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.display_products()
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.remove_from_cart()
            elif choice == '4':
                self.cart.view_cart()
            elif choice == '5':
                self.checkout()
            elif choice == '6':
                self.low_stock_alert()
            elif choice == '7':
                print("=====Exiting, Thank You For Using BEST BUY RETAIL STORE POS SYSTEM=====")
                break
            else:
                print("Invalid option. Try again.")

if __name__ == "__main__":
    pos =POS()
    pos.run()






