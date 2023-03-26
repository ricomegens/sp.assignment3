import random
import querie_runner as qr
import products as pd

def profile():
    # select all profile ids
    profiles = """SELECT profile.id FROM profile"""
    get_profiles = qr.run_query(profiles, fetch=True)
    # run query and put them in a list, return a random profile
    all_profiles = [profile for profile in get_profiles]
    return random.choice(all_profiles)

def similar_products(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    similar = """SELECT product_id FROM similars, profile, product WHERE profile.id = %s AND similars.profile_id
        = profile.id AND similars.product_id = product.id AND product.stock > 0 AND product.recommendable = True"""
    get_similar = qr.run_query(similar, profile, True)
    # if a profile has no similar products
    if len(get_similar) == 0:
        print("No similar products found")
        return
    print(f"Simlar products found\n {get_similar}")
    return

def viewed_before(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    viewed_before = """SELECT product.id FROM viewed_before, product, profile WHERE profile.id = %s
        AND viewed_before.profile_id = profile.id AND viewed_before.product_id = product.id AND
        product.recommendable = True AND product.stock > 0"""
    get_viewed_before = qr.run_query(viewed_before, profile)
    # if a profile has no previously seen products
    if not get_viewed_before:
        print("No previously seen products to be retrieved")
        return
    print(f"Previously seen products retrieved\n{get_viewed_before}")
    return get_viewed_before

def similar_to_viewed_before(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    # try and except for when viewed_before function returns nothing (no previously seen products for profile)
    try:
        for viewed in viewed_before(profile):
            similar_to_viewed = [row for row in pd.product_recommendations(viewed)]
        print(f"Products\n{similar_to_viewed}")
        return
    except TypeError:
        return

def products_ordered_recommendations(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    # Retrieving the products ordered
    ordered = """SELECT product_ordered.product_id FROM product_ordered, session, buid, profile
    WHERE profile.id = buid.profile_id AND profile.id = %s AND buid.id = session.buid_id AND 
    session.id = product_ordered.session_id"""
    get_ordered = qr.run_query(ordered, profile, True)
    # If no products are ordered
    if not get_ordered:
        print("No products ordered")
        return
    # Get the preference ids of the ordered products and retrieve new product ids from them
    for order in get_ordered:
        get_products = [row for row in pd.product_recommendations(order)]
    print(f"Retrieved similar to ordered products\n{get_products}")
    return

def recommend_long_events(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    # get events longer than 30s in which a product was looked at
    long_events = """SELECT event.id FROM session, buid, profile, event WHERE profile.id = %s AND 
                        profile.id = buid.profile_id AND buid.id = session.buid_id AND session.id = event.session_id
                        AND event.time_on_page > 30"""
    get_long_events = qr.run_query(long_events, profile, True)
    # if a profile has no events in which this is the case
    if len(get_long_events) == 0:
        print("No relevant events found")
        return
    print(f"Retrieved event ids \n{get_long_events}")
    products_interested = """SELECT product.id FROM product, session WHERE event.id = %s AND event.productid
                            = product.id AND product.stock > 0"""
    # Loop through incase of multiple events
    for event in get_long_events:
        interested = [product[0] for product in qr.run_query(products_interested, event, True)]
    print(f"Products customer took a long interest in\n{interested}")
    return

# TO DO
def session_preference(profile= None):
    if not profile:
        profile = profile_id
    # get events shorter than 30s in which a product was looked at
    events = """SELECT event.id FROM session, buid, profile, event WHERE profile.id = %s AND 
                profile.id = buid.profile_id AND buid.id = session.buid_id AND session.id = event.session_id
                AND event.time_on_page < 30"""
    get_event_ids = qr.run_query(events, profile, True)
    # Incase a profile has no events
    if len(get_event_ids) == 0:
        print("No relevant events found")
        return
    print(f"Retrieved event ids \n{get_event_ids}")
    # Get the product ids of these events
    prod_ids = """SELECT product.id FROM product, session, event WHERE event.id = %s AND event.product_id
                        = product.id"""
    for event in get_event_ids:
        products_ids = [product for product in qr.run_query(prod_ids, event, True)]
    # Loop through these product ids and get the preference ids to get product ids to recommend
    for id in products_ids:
        products_similar_to_seen = [row for row in pd.product_recommendations(id)]

    print(f"Products customer also might be interested in according to session\n{products_similar_to_seen}")
    return

def previously_recommended(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    previously_recommend = """SELECT product.id FROM product, previously_recommended, profile WHERE
                                profile.id = %s AND profile.id = previously_recommended.profile_id AND
                                previously_recommended.product_id = product.id AND product.stock > 0 
                                AND product.recommendable = True"""
    get_previously_recommended = qr.run_query(previously_recommend, profile, True)
    # if a profile has no previously recommended products
    if len(get_previously_recommended) == 0:
        print('No product founds')
        return
    print(f'Products previously recommended\n{get_previously_recommended}')
    return get_previously_recommended

def similar_to_previously_recommended(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    # return nothing in case of a TypeError, which means no previously recommended products
    try:
        prev_recommend = previously_recommended(profile)
        for product in prev_recommend:
            prods = [row[0] for row in pd.product_recommendations(product)]
        print(f"Products\n{prods}")
        return
    except TypeError:
        return

def new_profile(profile= None):
    # if no input given, use the random selected profile id
    if not profile:
        profile = profile_id
    # return product ids based on if there is stock, it is recommendable and if customers buy it on repeat
    random_product = """SELECT product.id FROM product WHERE product.stock > 0 AND product.recommendable
                        = True AND product.herhaalaankopen = True"""
    get_random_product = qr.run_query(random_product, profile, True)
    print(f"Products recommended\n{get_random_product}")
    return


if __name__ == "__main__":
    profile_id = profile()
    similar_products()
    viewed_before()
    similar_to_viewed_before()
    products_ordered_recommendations()
    recommend_long_events()
    session_preference()
    previously_recommended()
    similar_to_previously_recommended()
    new_profile()