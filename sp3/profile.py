import random
import querie_runner as qr


def profiles():
    profiles = """SELECT profile.id FROM profile"""
    get_profiles = qr.run_query(profiles, fetch=True)
    all_profiles = {profile for profile in get_profiles}
    return

def similar_products(profile= None):
    if profile == None:
        random.choice(profile)
    similar = """SELECT product_id FROM similars, profile, product WHERE profile.id = (%) AND similars.profileid
        = profile.id AND similars.productid = product.id AND product.stock > 0"""
    print("Looking for similar products based on profile")
    get_similar = qr.run_query(similar, profile, True)
    print(f"Simlar products found\n {get_similar}")
    return

def viewed_before(profile= None):
    viewed_before = """SELECT product.id FROM viewed_before, product, stock, profile WHERE profile.id = (%)
        viewed_before.profile_id = profile.id AND viewed_before.product_id = product.id AND 
        product.stock > 0"""
    print("Retrieving previously seen products")
    get_viewed_before = qr.run_query(viewed_before)
    print(f"Previously seen products retrieved\n{get_viewed_before}")
    return

def products_ordered_recommendations(profile= None):
    ordered = """SELECT products_ordered.productid FROM products_ordered, session, buid, profile
    WHERE profile.id = buid.profileid AND profile.id = (%) AND buid.id = session.buidid AND 
    session.id = products_ordered.sessionid"""
    print("Getting products ordered")
    get_ordered = qr.run_query(ordered, profile, True)
    random_product = random.choice(get_ordered)
    preference_id = """SELECT preference.id FROM preference, product, product_preference
    WHERE product.id = (%) and product.id = product_preference.productid AND product_preference.preferenceid = 
    preference.id"""
    get_pref_id = qr.run_query(preference_id, random_product, True)
    print(f"Retrieved similar products")
    products = """SELECT product.id FROM product, product_preference, preference WHERE preference.id = (%)
    AND preference.id = product_preference.preferenceid AND product_preference.productid = product.id"""
    get_products = qr.run_query(products, get_pref_id, True)
    print(f"Retrieved similar to ordered products\n{get_products}")
    return

def profile_recommendations(profile= None):
    similar_to_viewed_before = """SELECT product.id from product, viewed_before, profile, product_preference,
     preference, stock WHERE profile.id = viewed_before.profileid AND viewed_before.productid = preference"""
    # TO DO
    session_preference = """SELECT product_id FROM preference, session_preference, session, buid, profile,
     event WHERE profile.id = buid.profile_id and buid.id = session.buid_id and session.id = 
     session_preference.session_id and session.id = event.session_id AND session_preference.preferenceid = preference.id"""