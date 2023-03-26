import querie_runner as qr
import random

def product_ids():
    ids = """SELECT product.id FROM product"""
    print("Getting all product ids")
    get_ids = qr.run_query(ids)
    products = [id for id in get_ids]
    print("All product ids retrieved")
    return random.choice(products)

def product_recommendations(product= None):
    # If no product id is inserted, choose the random one
    if not product:
        product = ids
    # SQL statements to get the preference id and product id
    preference_id = """SELECT preference.id FROM preference, product_preference, product WHERE product.id = %s 
    AND preference.id = product_preference.preference_id and product_preference.product_id = product.id"""
    get_products = """SELECT product.id FROM product, product_preference, preference WHERE preference.id = %s AND 
    preference.id = product_preference.preference_id AND product_preference.product_id = product.id"""
    get_preference_id = qr.run_query(preference_id, product)
    print(f"Succesful, getting similar products from preferenceid: {get_preference_id}")
    # product can have multiple preference ids, loop through and use the product id
    # SQL statement to get new product ids
    for pref_id in get_preference_id:
        products = [row for row in qr.run_query(get_products, pref_id)]

    print(f"Products retrieved\n {products}")
    return

if __name__ == "__main__":
    ids = product_ids()
    print(ids)
    product_recommendations()