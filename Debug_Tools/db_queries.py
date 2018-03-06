import pymongo
from bson.objectid import ObjectId


# Returns a document db object for a specific document id.
def get_document_with_id(doc_id, current_week):
    # Getting data from the mongo database
    client = pymongo.MongoClient()
    # Database name is minedNews
    db = client.minedArticles

    document = db[current_week].find({"_id": ObjectId(doc_id)})

    return document
