class Inventory():
    def __init__(self):
        self.products = [
        {
            "id" : "001",
            "name" : "Boob Print Face Masks | Valentine's Mask",
            "price" : 5.00
        },

        {
            "id" : "002",
            "name" : "Small Pink Strawberry Print Cosmetic Pouch",
            "price" : 8.00
        },

        {
            "id" : "003",
            "name" : "Cow Print Fabric Face Mask",
            "price" : 5.00
        },

        {
            "id" : "004",
            "name" : "Large Dinosaur Print Cosmetic Bag",
            "price" : 12.00
        },

        {
            "id" : "005",
            "name" : "Large Cherry Print Cosmetic Bag",
            "price" : 12.00
        },

        {
            "id" : "006",
            "name" : "Cherry Print Fabric Face Mask",
            "price" : 5.00
        },

        {
            "id" : "007",
            "name" : "Medium Pink Big Cat Print Cosmetic Bag",
            "price" : 10.00
        },

        ]
    # Product fetching function for the add to cart functionality.

    def get_one(self, item_id):
        p = [p for p in self.products if p["id"] == item_id]
        if len(p) > 0:
            return p[0]
        return False    

