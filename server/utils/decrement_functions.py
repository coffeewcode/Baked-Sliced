def decrement_stock_default(self, requested_quantity, message):
    if self.stock_quantity >= requested_quantity:
        self.stock_quantity -= requested_quantity
        self.save()
    else:
        raise ValueError(f"There is no more {message}. The stock available is 0. ")
