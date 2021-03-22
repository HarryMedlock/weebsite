import stripe

def retrieve_product(product_id) -> [Product]:
    return stripe.Product.retrieve(product_id)