import random
import querie_runner as qr


def profile():
    profiles = """SELECT profile.id FROM profile"""
    get_profiles = qr.run_query(profiles, fetch=True)
    all_profiles = [profile for profile in get_profiles]
    return random.choice(all_profiles)

def similar_products(profile= None):
    if not profile:
        profile = id
    similar = """SELECT product_id FROM similars, profile, product WHERE profile.id = %s AND similars.profile_id
        = profile.id AND similars.product_id = product.id AND product.stock > 0 AND product.recommendable = True"""
    print("Looking for similar products based on profile")
    get_similar = qr.run_query(similar, profile, True)
    if len(get_similar) == 0:
        print("No similar products found")
    print(f"Simlar products found\n {get_similar}")
    return

def viewed_before(profile= None):
    if not profile:
        profile = id
    viewed_before = """SELECT product.id FROM viewed_before, product, profile WHERE profile.id = %s
        AND viewed_before.profile_id = profile.id AND viewed_before.product_id = product.id AND
        product.recommendable = True AND product.stock > 0"""
    print("Retrieving previously seen products")
    get_viewed_before = qr.run_query(viewed_before, profile)
    if not get_viewed_before:
        print("No previously seen products to be retrieved")
        return
    print(f"Previously seen products retrieved\n{get_viewed_before}")
    return

def products_ordered_recommendations(profile= None):
    if not profile:
        profile = id
    ordered = """SELECT product_ordered.product_id FROM product_ordered, session, buid, profile
    WHERE profile.id = buid.profile_id AND profile.id = %s AND buid.id = session.buid_id AND 
    session.id = product_ordered.session_id"""
    print("Getting products ordered")
    get_ordered = qr.run_query(ordered, profile, True)
    if not get_ordered:
        print("No products ordered")
        return
    random_product = random.choice(get_ordered)
    preference_id = """SELECT preference.id FROM preference, product, product_preference
    WHERE product.id = %s and product.id = product_preference.product_id AND product_preference.preference_id = 
    preference.id"""
    get_pref_id = qr.run_query(preference_id, random_product, True)
    print(f"Retrieved similar products")
    products = """SELECT product.id FROM product, product_preference, preference WHERE preference.id = %s
    AND preference.id = product_preference.preference_id AND product_preference.product_id = product.id"""
    # incase product has multiple preference ids
    for pref_id in get_pref_id:
        get_products = [qr.run_query(products, pref_id, True)]
    print(f"Retrieved similar to ordered products\n{get_products}")
    return

def recommend_long_events(profile= None):
    if not profile:
        profile = id
    long_events = """SELECT event.id FROM session, buid, profile, event WHERE profile.id = %s AND 
                        profile.id = buid.profile_id AND buid.id = session.buid_id AND session.id = event.session_id
                        AND event.time_on_page > 30"""
    get_long_events = qr.run_query(long_events, profile, True)
    if len(get_long_events) == 0:
        print("No relevant events found")
        return
    print(f"Retrieved event ids \n{get_long_events}")
    products_interested = """SELECT product.id FROM product, session WHERE event.id = %s AND event.productid
                            = product.id AND product.stock > 0"""
    # Loop through incase of multiple events
    for event in get_long_events:
        interested = [product for product in qr.run_query(products_interested, event, True)]
    print(f"Products \n{interested}")
    return

# TO DO
def session_preference(profile= None):
    if not profile:
        profile = id
    events = """SELECT event.id FROM session, buid, profile, event WHERE profile.id = %s AND 
                profile.id = buid.profile_id AND buid.id = session.buid_id AND session.id = event.session_id"""
    profile = ("5c1233268d522a0001610a0a",)
    get_event_ids = qr.run_query(events, profile, True)
    # Incase a profile has no events
    if len(get_event_ids) == 0:
        print("No relevant events found")
        return
    print(f"Retrieved event ids \n{get_event_ids}")
    # Loop through incase of multiple events
    prod_ids = """SELECT product.id FROM product, session, event WHERE event.id = %s AND event.product_id
                        = product.id"""
    for event in get_event_ids:
        products_ids = [product for product in qr.run_query(prod_ids, event, True)]
    get_preference_ids = """SELECT preference.id FROM preference, product, product_preference WHERE
                            product.id = %s AND product.id = product_preference.product_id AND 
                            product_preference.preference_id = preference.id"""
    for id in products_ids:
        preference_ids = [preference for preference in qr.run_query(get_preference_ids, id, True)]
    get_products = """SELECT product.id FROM product, preference, product_preference WHERE preference.id
                        = %s AND preference.id = product_preference.preference_id AND 
                        product_preference.product_id = product.id"""
    for pref in preference_ids:
        products_similar_to_seen = [row for row in qr.run_query(get_products, pref, True)]

    print(f"Products \n{products_similar_to_seen}")
    return

if __name__ == "__main__":
    id = profile()
    # similar_products()
    # viewed_before()
    # products_ordered_recommendations()
    # recommend_long_events()
    session_preference()