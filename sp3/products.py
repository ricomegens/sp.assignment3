import querie_runner as qr
import random

def product_ids():
    ids = """SELECT product.id FROM product"""
    print("Getting all product ids")
    get_ids = qr.run_query(ids, fetch=True)
    products = [id for id in get_ids]
    print("All product ids retrieved")
    return products

def product_recommendations(product= None):
    if not product:
        product = random.choice(ids)
    preference_id = """SELECT preference.id FROM preference, product_preference, product WHERE product.id = %s 
    AND preference.id = product_preference.preference_id and product_preference.product_id = product.id"""
    get_products = """SELECT product.id FROM product, product_preference, preference WHERE preference.id = %s AND 
    preference.id = product_preference.preference_id AND product_preference.product_id = product.id"""
    print("Getting preference_id from giving product")
    get_preference_id = qr.run_query(preference_id, product, True)
    print(f"Succesful, getting similar products from preferenceid: {get_preference_id}")
    # product can have multiple preference ids, loop through
    for pref_id in get_preference_id:
        products = [row for row in qr.run_query(get_products, pref_id, True)]

    print(f"Products retrieved\n {products}")
    return

if __name__ == "__main__":
    ids = product_ids()
    product_recommendations()