from os import getenv
from utils import flist
import pandas as pd


def get_watch_list(db):
    inv_film = {
        i['inventory_id']: i['film_id']
        for i in db.inventory.find()
    }

    watch_list = dict()
    for cid in flist(db.rental.find()).map(lambda r: r['customer_id']):
        if cid not in watch_list:
            watch_list[cid] = set()
        watch_list[cid].add(inv_film[cid])

    return watch_list


def get_recomendators(db, watch_list, usr_id):
    watched = watch_list[usr_id]
    return {
        cid: flist(watched).filter(lambda f: f in watch_list[cid]).len()
        for cid in
        flist(watch_list).filter(
            lambda cid: cid != usr_id and len(watch_list[cid]) >= len(watched)
        )
    }


def get_recomendations(db, watch_list, recomendators, usr_id):
    watched = watch_list[usr_id]
    good_films = dict()

    for cust in recomendators.keys():
        for film in flist(watch_list[cust]) \
              .filter(lambda f: f not in watched):
            good_films[film] = good_films.get(film, 0) + 1

    return good_films


# A report that, given a certain customer (parameter) and his/her historical
# data on rented movies, recommends other movies. Such a recommendation should
# be based on customers that watched similar sets of movies. Create a metric
# (any) to assess to which degree a movie is a good recommendation.
def query(db):
    usr_id = int(getenv("CUSTOMER_ID"))
    watch_list = get_watch_list(db)
    good_recomendators = get_recomendators(db, watch_list, usr_id)
    good_films = get_recomendations(db, watch_list, good_recomendators, usr_id)

    top = flist(list(good_films.items())) \
        .sort(key=lambda kv: kv[1], reverse=True) \
        .map(lambda kv: (db.film.find_one({'film_id': kv[0]})['title'], kv[1]))

    usr = db.customer.find_one({'customer_id': usr_id})
    print(f"Customer name: {usr['first_name']} {usr['last_name']}")
    print(pd.DataFrame(top, columns=('Film title', 'mark')))
