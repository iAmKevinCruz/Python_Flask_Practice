import pymongo

# connection string
# on the job tit'll look like this:
# # mongo_url = "mongodb+srv://.........."
# FREE SERVICE: mongodb.net
mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)
# db points to the actual data base
db = client.get_database("storeData")
