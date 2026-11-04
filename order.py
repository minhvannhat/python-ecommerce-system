from product import Product
from inventory import Inventory

class Order:
    def __init__(self,inventory):
        self.inventory = inventory
        self.items = []
        self.checked_out = False
        self.cancelled = False

    def add_item(self, product_id, quantity):
        if self.checked_out or self.cancelled:
            return False
        
        product = self.inventory.get_product(product_id)

        if product is None:
            return False
        if int(quantity) <= 0 or not isinstance(quantity,int) or isinstance(quantity,bool):
            return False

        self.items.append((product, quantity))
        return True

    def remove_item(self,product_id):
        if self.checked_out or self.cancelled:
            return False
        
        for item in self.items:
            if item[0].product_id == product_id:
                self.items.remove(item)
                return True
        return False

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item[1] * item[0].price
        return total

    def checkout(self):
        if self.checked_out or len(self.items) == 0 or self.cancelled:
            return False

        in_cart = {}

        for item in self.items:
            product_id = item[0].product_id
            quantity = item[1]
            in_cart[product_id] = in_cart.get(product_id, 0) + quantity

        for item in self.items:
            if in_cart[item[0].product_id] > item[0].quantity:
                return False
            
        for product_id, quantity in in_cart.items():
            product = self.inventory.get_product(product_id)
            if product is None:
                return False
            
            product.sell(quantity)

        self.checked_out = True

        return self.calculate_total()

    def update_quantity(self, product_id, new_quantity):
        if self.checked_out or self.cancelled or not isinstance(new_quantity,int) or isinstance(new_quantity,bool) or int(new_quantity) <= 0:
            return False
        
        for i, item in enumerate(self.items):
            if item[0].product_id == product_id:
                self.items[i] = (item[0],new_quantity)
                return True

        return False

    def print_receipt(self):
        if not self.checked_out:
            print("You haven't checked out")
            return False
        
        cart = {}

        for item in self.items:
            product_id = item[0].product_id
            quantity = item[1]

            cart[product_id] = cart.get(product_id, 0) + quantity

        print("========== RECEIPT ==========")
        for product_id, y in cart.items():
            product = self.inventory.get_product(product_id)
            print(f"  {product.name}     x{y}    ${product.price*y:.2f}")
        print("-----------------------------")
        print(f"Total:               ${self.calculate_total():.2f}")

        if self.cancelled:
            print("\nStatus: Cancelled")
        elif self.checked_out:
            print("Status: Completed")

        print("=============================")
        return True

    def cancel_order(self):
        if self.cancelled or not self.checked_out:
            return False
        elif self.checked_out:
            for item in self.items:
                item[0].restock(item[1])
                self.cancelled = True
            print("Order is cancelled")
            return True