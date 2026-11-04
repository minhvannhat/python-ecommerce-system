from inventory import Inventory
from order import Order
from product import Product

class Store:
    def __init__(self):
        self.inventory = Inventory()

        self.order = Order(self.inventory)
        self.order_history = []

        self.running = False

        self.setup_products()

    def run(self):
        self.running = True
        while self.running:
            try:
                choose = int(input(self.show_menu()))
            except ValueError:
                print("Please enter a number\n")
                continue
            print()

            if not 1 <= choose <= 11:
                print("Invalid input\n")
                continue
            elif choose == 11:
                self.running = False
                return

            actions = {
                1: self.view_products,
                2: self.add_to_cart,
                3: self.remove_from_cart,
                4: self.update_product_quantity,
                5: self.view_cart,
                6: self.checkout,
                7: self.view_receipt,
                8: self.cancel_order,
                9: self.new_order,
                10: self.view_order_history
            }

            action = actions.get(choose)
            if action:
                action()
                print()
            else:
                print("Invalid choice")
                return False

    def show_menu(self):
        return """========== E-COMMERCE STORE ==========

1. View Available Products
2. Add Product to Cart
3. Remove Product from Cart
4. Update Product Quantity
5. View Shopping Cart
6. Checkout
7. View Order Receipt
8. Cancel Order
9. New order
10. View order history
11. Exit

Choose: """

    def new_order(self):
        if not self.order.checked_out and not self.order.cancelled:
            print("Can't create new order")
            return False

        self.order_history.append(self.order)

        order = Order(self.inventory)
        self.order = order

        print("New order created")
        return True

    def view_order_history(self):
        if not len(self.order_history) > 0:
            print("History is empty")
            return False
         
        for index, order in enumerate(self.order_history):
            print(index + 1,".")
            order.print_receipt()
            print()

    def view_products(self):
        self.inventory.list_products()

    def add_to_cart(self):
        try:
            product_id = int(input("Enter product ID: "))
        except ValueError:
            print("Please enter a number\n")
            return False
        
        try: 
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Please enter a number\n")
            return False

        if not self.order.add_item(product_id, quantity):
            print("Can't add item to cart\n")
            return False
        return True

    def remove_from_cart(self):
        try:
            product_id = int(input("Enter product ID: "))
        except ValueError:
            print("Please enter a number\n")
            return False
        
        if not self.order.remove_item(product_id):
            print("Can't remove product")
            return False
        return True

    def update_product_quantity(self):
        try:
            product_id = int(input("Enter product ID: "))
        except ValueError:
            print("Please enter a number\n")
            return False

        try:
            new_quantity = int(input("New quantity: "))
        except ValueError:
            print("Please enter a number\n")
            return False

        if not self.order.update_quantity(product_id, new_quantity):
            print("Can't update quantity")
            return False
        return True

    def view_cart(self):
        if not len(self.order.items) > 0:
            print("\nCart is empty")
            return False
        
        for index, item in enumerate(self.order.items):
            print(f"{index + 1}. {item[0].name} | x {item[1]}")
        return True

    def checkout(self):
        self.order.checkout()
        if self.order.checked_out:
            print("Checked out")
        else:
            print("Can't check out")

    def view_receipt(self):
        self.order.print_receipt()

    def cancel_order(self):
        if not self.order.cancel_order():
            print("Can't cancel order")
            return False
        return True

    def setup_products(self):
        products = [
            Product(1, "Laptop", 1200, 10),
            Product(2, "Keyboard", 80, 25),
            Product(3, "Mouse", 40, 30),
            Product(4, "Monitor", 300, 15),
            Product(5, "Headphones", 150, 20)
        ]

        for product in products:
            self.inventory.add_product(product)
