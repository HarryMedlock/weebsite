from app.inventory import Inventory


class Cart(object):

    def __init__(self, cart_dict=None):

        cart_dict = cart_dict or {}
        
        if cart_dict == {}:
            self.total = 0
            self.items = []
        else: 
            self.total = cart_dict["total"]
            self.items = cart_dict["items"]
        
    def to_dict(self):

        return {
            "total" : self.total,
            "items" : self.items
        }
    
    def change_item(self, item_id, operation):

        product = Inventory().get_one(item_id)

        if product:
            if operation == 'add':
                self.items.append(product)
            elif operation == 'remove':
                cart_p = [x for x in self.items if x['id'] == product['id']]
                self.items.remove(cart_p[0])
                self.update()
                return True
            else:
                return False

    def update(self):

        total = float(0)
        for product in self.items:
            total += float(product['price'])
        self.total = total