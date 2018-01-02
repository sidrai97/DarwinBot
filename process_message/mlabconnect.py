uri='mongodb://heroku_56wpj1hj:bhqlfc9t48iqeoiqmobf6i5k1q@ds243295.mlab.com:43295/heroku_56wpj1hj'
from pymongo import MongoClient

client=MongoClient(uri,connectTimeoutMS=30000,socketTimeoutMS=None,socketKeepAlive=True)
db=client.darwin
collection=db.users
collection.insert_one({"_id":"abcd","name":"sid"})