import pymongo

'''
Remove all collection(s) and Create new empty collection(s)
Detailed implementation is in phase 3

Param: None
Output: 
    successful messages or failure messages for exceptions
'''
def collection_drop_create():
    
    with open("config-MongDB.txt") as f:
        address = f.read()
    
    try:
        client = pymongo.MongoClient(address)
        db = client['university']        
        db.course.drop()       
        client.close()
    except pymongo.errors.ConnectionFailure as error: 
        print(error)


    
    print("Collection dropping and empty collection creating are successful")
    return





#Interface

def collection_handler():
    collection_drop_create()
    return 