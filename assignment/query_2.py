from utils import bd_map, flist
import pandas as pd


# Create a report that shows a table actor (rows) vs actor (columns)
# with the number of movies the actors co-starred.
def query(db):
    # Returns dict with film_id as key and set of actor_id's
    film_actors = bd_map(db.film_actor.find(), 'film_id', 'actor_id')

    co_star = dict()
    for actors in film_actors.values():
        for a1 in actors:
            for a2 in actors:
                if a1 == a2:
                    continue
                if a1 not in co_star:
                    co_star[a1] = dict()
                co_star[a1][a2] = co_star[a1].get(a2, 0) + 1

    raw_report = pd.DataFrame(co_star)
    report = raw_report.fillna(0).astype(int).sort_index().sort_index(axis=1)
    pd.set_option('display.max_columns', 10)
    print(report)
