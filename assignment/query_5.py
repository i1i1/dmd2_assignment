import pandas as pd
from utils import bd_map
from os import getenv


# Create a report that shows the degrees of separation between a certain actor
# (choose one, this should be fixed) and any other actor.
def query(db):
    def dfs(bacon, actors):
        film_actors = bd_map(db.film_actor.find(), 'film_id', 'actor_id')
        actor_films = bd_map(db.film_actor.find(), 'actor_id', 'film_id')

        while actors:
            choosen = actors.pop()
            for film in actor_films[choosen]:
                for actor in film_actors[film]:
                    if actor not in bacon:
                        actors.append(actor)
                        bacon[actor] = bacon[choosen] + 1
                    else:
                        bacon[actor] = min(bacon[actor], bacon[choosen]+1)

    choosen_actor = int(getenv("ACTOR_ID"))
    bacon = {choosen_actor: 0}
    dfs(bacon, [choosen_actor])
    report = pd.DataFrame \
               .from_dict(bacon, orient='index', columns=['Bacon number']) \
               .sort_index()
    report.index.name = 'Actor id'
    print(report)
