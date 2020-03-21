import pandas as pd
from utils import bd_map, flist


# A report that lists all films, their film category and
# the number of times it has been rented by a customer.
def query(db):
    film_inventory = bd_map(db.inventory.find(), 'film_id', 'inventory_id')
    film_cat = {f['film_id']: f['category_id'] for f in db.film_category.find()}
    film_title = {f['film_id']: f['title'] for f in db.film.find()}
    cat_name = {c['category_id']: c['name'] for c in db.category.find()}

    inv_times_rented = dict()
    for rent in db.rental.find():
        iid = rent['inventory_id']
        inv_times_rented[iid] = inv_times_rented.get(iid, 0) + 1

    df = sorted([
        (
            film_title[f],
            cat_name[film_cat[f]],
            flist(inv).map(lambda iid: inv_times_rented.get(iid, 0)).sum(),
        ) for f, inv in film_inventory.items()
    ], key=lambda x: x[2], reverse=True)

    print(pd.DataFrame(df, columns=('title', 'category', 'times rented')))
