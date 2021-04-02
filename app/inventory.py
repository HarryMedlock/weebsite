class Inventory():
    def __init__(self):
        self.products = [
        {
            "id" : "001",
            "name" : "Boob Print Face Masks | Valentine's Mask",
            "price" : "5.00",
            "type" : "masks",
            "picture" : "boob_mask_1.jpg",
            "link" : "purchase_boob",
        },

        {
            "id" : "002",
            "name" : "Small Pink Strawberry Print Cosmetic Pouch",
            "price" : "8.00",
            "type" : "bags",
            "picture" : "strawb_bag.jpg",
            "link" : "purchase_strawb"
        },

        {
            "id" : "003",
            "name" : "Cow Print Fabric Face Mask",
            "price" : "5.00",
            "type" : "masks",
            "picture" : "cow_mask.jpg",
            "link" : "purchase_cow"
        },

        {
            "id" : "004",
            "name" : "Large Dinosaur Print Cosmetic Bag",
            "price" : "12.00",
            "type" : "bags",
            "picture" : "dinosaur.jpg",
            "link" : "purchase_dino"
        },

        {
            "id" : "005",
            "name" : "Large Cherry Print Cosmetic Bag",
            "price" : "12.00",
            "type" : "bags",
            "picture" : "cherry.jpg",
            "link" : "purchase_cherry"
        },

        {
            "id" : "006",
            "name" : "Cherry Print Fabric Face Mask",
            "price" : "5.00",
            "type" : "masks",
            "picture" : "cherry_mask.jpg",
            "link" : "purchase_cherrymask"
        },

        {
            "id" : "007",
            "name" : "Medium Pink Big Cat Print Cosmetic Bag",
            "price" : "10.00",
            "type" : "bags",
            "picture" : "bigcat_bag.jpg",
            "link" : "purchase_cat"
        },

        ]

    def get_all(self):
        return self.products
    # Product fetching function for the add to cart functionality.

    def get_one(self, item_id):
        p = [p for p in self.products if p["id"] == item_id]
        if len(p) > 0:
            return p[0]
        return False    

