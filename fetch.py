from random import random
import foursquare
import fire
import os
import pymongo


def env(key):
    if not key in os.environ:
        print('No %s' % key)
        exit()
    return os.environ[key]


BB_TL = (59.8946, 29.8735)
BB_BR = (59.8657, 29.9534)


def random_coord():
    def randrange(start, end):
        return start + random() * (end - start)

    lat = randrange(BB_BR[0], BB_TL[0])
    lon = randrange(BB_BR[1], BB_TL[1])
    return lat, lon


client_id = env('CLIENT_ID')
client_secret = env('CLIENT_SECRET')
db_path = env('DB')
db_name = env('DB_NAME')

client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret)
mongo = pymongo.MongoClient(db_path)[db_name]


def venues(number):
    for i in range(number):
        ll = random_coord()
        query = {
            'll': '%s,%s' % ll,
            'limit': 50
        }
        
        res = client.venues.search(params=query)
        venues = res['venues']
        print(i, ll, len(venues))

        for v in venues:
            vid = v['id']
            mongo.venues.update({'id': vid}, v, upsert=True)

if __name__ == '__main__':
    fire.Fire()
