# mongodb_handler.py
import pymongo # type: ignore

class MongoDBHandler:
    def __init__(self, mongo_url):
        self.mongo_url = mongo_url

    def store_data(self, data):
        try:
            print('Mongoose url provided', self.mongo_url)
            client = pymongo.MongoClient(self.mongo_url)
            db = client["scraper_db"]
            collection = db["products"]

            # Prepare bulk operations
            bulk_operations = []
            for product in data:
                if product.get("id"):
                    # Create a filter for the update operation
                    filter_query = {"product_id": product["id"]}
                    # Create an update document
                    update_doc = {"$set": {"product_id" : product["id"], "product_title" : product["title"], "product_price" : product["price"], "product_image" : product["image"]}}
                    # Append the update operation to the list of bulk operations
                    bulk_operations.append(pymongo.UpdateOne(filter_query, update_doc, upsert=True))

            # Execute bulk write operations
            result = collection.bulk_write(bulk_operations)

            print(f"{result.upserted_count} products inserted, {result.modified_count} products updated in MongoDB")
        except Exception as e:
            print(f"Error occurred while storing data in MongoDB: {str(e)}")
