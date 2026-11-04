from product import Product

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self,product):
        if product.product_id not in self.products:
            self.products[product.product_id] = product

    def get_product(self,product_id):
        return self.products.get(product_id)

    def remove_product(self,product_id):
            self.products.pop(product_id,None)

    def list_products(self):
        for product in self.products.values():
            print(product)
    