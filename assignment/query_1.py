from utils import flist, bd_map
import pandas as pd


# Retrieve all the customers that rented movies of at least
# two different categories during the current year
def query(db):
    year = flist(db.rental.find()).map(lambda x: x['rental_date'].year).max()
    year_items = flist(db.rental.find()) \
        .filter(lambda x: x['rental_date'].year == year)
    inv_film = {i['inventory_id']: i['film_id'] for i in db.inventory.find()}
    film_cat = {f['film_id']: f['category_id'] for f in db.film_category.find()}

    # Dict from customers to all categories which they watched
    customers = {
        cid: set(flist(inv).map(lambda iid: film_cat[inv_film[iid]]))
        # Returns dict with customer_id as key and set of actor_id's
        for cid, inv in bd_map(year_items, 'customer_id', 'inventory_id').items()
    }

    customers = flist(customers.items()) \
        .filter(lambda kv: len(kv[1]) >= 2) \
        .map(lambda kv: db.customer.find_one({'customer_id': kv[0]})) \
        .map(lambda c: (c['first_name'], c['last_name']))

    print(pd.DataFrame(customers, columns=('Name', 'Surname')))
