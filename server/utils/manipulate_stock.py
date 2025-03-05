def decrement_stock_default(self, requested_quantity, message="elements"):
    if self.stock_quantity >= requested_quantity:
        self.stock_quantity -= requested_quantity
        self.save()
    else:
        raise ValueError(f"There is no more {message}. The stock available is 0. ")


def increment_stock_default(self, quantity_to_add):
    self.stock_quantity += quantity_to_add
    self.save()


def validate_stock_update(self, new_quantity, instance, attr):
    if new_quantity != instance.quantity:
        if new_quantity > instance.quantity:
            attr.increment_stock(instance.quantity)
            attr.decrement_stock(new_quantity)
        else:
            attr.increment_stock(instance.quantity - new_quantity)
