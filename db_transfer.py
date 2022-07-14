from pymongo import MongoClient
import pymongo



warehouse_db = cluster["WAREHOUSE_MANAGEMENT_GOODWILL"]
Truck_Receiver_DB = warehouse_db["Truck_Receiver_DB"]


Processor_Review_DB = warehouse_db["Processor_Review_DB"]


Jewelry_DB = warehouse_db["Jewelry_DB"]
Jewelry_Review_DB = warehouse_db["Jewelry_Review_DB"]

Books_Media_DB = warehouse_db["Books_Media_DB"]
Book_Media_Review_DB = warehouse_db["Book_Media_Review_DB"]

Finished_DB = warehouse_db["Finished_DB"]

Finished_Jewlery_DB = warehouse_db["Finished_Jewlery_DB"]



warehouse_db = cluster["WAREHOUSE_MANAGEMENT"]
#receiverCollection = warehouse_db["receiver"]

#processor_revCollection = warehouse_db["processor_rev"]


#jewleryCollection = warehouse_db["jewlery"]
#jewlery_revCollection = warehouse_db["jewlery_rev"]
FINISHEDCollection = warehouse_db["FINISHED"]

Finished_JewlCollection = warehouse_db["FINISHED_JEWL"]
for document in Finished_JewlCollection.find():
    print(document)
    Finished_Jewlery_DB.insert_one(document)
