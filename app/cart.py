from app.inventory import Inventory

class Cart(object):

    def __init__(self, cart_dict=None):

        cart_dict = cart_dict or {}
        
        if cart_dict = {}:
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
    
    