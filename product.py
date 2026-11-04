class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def restock(self, amount):
        if amount > 0:
            self.quantity += amount

    def sell(self,amount):
        if amount > 0 and amount <= self.quantity:
            self.quantity -= amount

    def __str__(self):
        return f"{self.product_id} | {self.name} | ${self.price:.2f} | Stock: {self.quantity}"
         