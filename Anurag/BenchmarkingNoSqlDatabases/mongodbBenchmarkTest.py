import json
from pymongo import MongoClient


#------------- Create db connection and create database ----------------------------

def create_connection():
    host_address = "localhost"
    port_no = "27017"
    username = "mongo"
    password = "secret"

    try:
        conn_string = "mongodb://"+username+":"+password+"@"+host_address+":"+port_no+"/" # <----enter username,pwd,host address and port no accordingly
        myclient = MongoClient(conn_string)
        print("Connected successfully!!!")
        print(myclient)
    except:
        print("Could not connect to MongoDB")

    return myclient

def createDB():
    myclient = create_connection()

    dblist = myclient.list_database_names()
    if "test" in dblist:
        print("The test database exists.")
    else:
        mydb = myclient["test"]

    myclient.close()

def createProfileCollection():
    myclient = create_connection()
    db = myclient.test
    profilesCollection = db["profiles"]
    print(db)
    myclient.close()

def createRelationsCollection():
    myclient = create_connection()
    db = myclient.test
    relationsCollection = db["relations"]
    print(db)
    myclient.close()

def insertIntoProfilesCollection():
    myclient = create_connection()
    db = myclient.test
    profileCol = db.profiles
    # Loading or Opening the json file
    with open('soc-pokec-profiles500.json',errors='ignore') as json_data:
        data = json.load(json_data)
    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else inser_one is used
    if isinstance(data, list):
        profileCol.insert_many(data)
    else:
        profileCol.insert_one(data)

    myclient.close()

def insertIntoRelationsCollection():
    myclient = create_connection()
    db = myclient.test
    relationsCol = db.relations
    # Loading or Opening the json file
    with open('soc-pokec-relationship5000.json',errors='ignore') as json_data:
        data = json.load(json_data)
    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else inser_one is used
    if isinstance(data, list):
        relationsCol.insert_many(data)
    else:
        relationsCol.insert_one(data)

    myclient.close()

def readProfilesCollection():
    myclient = create_connection()
    db = myclient.test
    mycol = db.profiles
    for x in mycol.find():
        print(x)

    myclient.close()

def readRelationsCollection():

    myclient = create_connection()
    db = myclient.test
    mycol = db.relations
    for x in mycol.find():
        print(x)
    myclient.close()


def dropProfilesCollection():
    myclient = create_connection()
    db = myclient.test
    mycol = db.profiles
    mycol.drop()
    print("profiles connection has been deleted.")
    myclient.close()

def dropRelationsCollection():
    myclient = create_connection()
    db = myclient.test
    mycol = db.relations
    mycol.drop()
    print("relations connection has been deleted.")
    myclient.close()

def dropDatabase():
    myclient = create_connection()
    myclient.drop_database('test')
    print("Test database has been deleted.")
    myclient.close()

def singleRead():
    myclient = create_connection()
    db = myclient.test
    mycol = db.profiles
    x = mycol.find_one()
    print(x)
    myclient.close()

def singleWrite():
    myclient = create_connection()
    db = myclient.test
    mycol = db.profiles
    with open('soc-pokec-profiles500.json',errors='ignore') as json_data:
        data = json.load(json_data)
    mycol.insert_one(data[400])
    myclient.close()

def aggregate():
    myclient = create_connection()
    db = myclient.test
    mycol = db.profiles
    aggregate_result = mycol.aggregate([{
                                        "$group":
                                            {
                                                "_id" : "&AGE",
                                                "Aggregate Age" : {"$sum":1}
                                            }
                                        }])


    for i in aggregate_result:
        print(i)
    myclient.close()

def neighbors():
    myclient = create_connection()
    db = myclient.test
    mycol = db.relations

    record = mycol.find({"_from" : '1'},{"_to": 1})

    for doc in record:
        print(doc)

    myclient.close()

def neighbors2():
    myclient = create_connection()
    db = myclient.test
    mycol = db.relations
    #this is sql query
    # sql_query = "select _to from relations where _from = '15' union" \
    #             " distinct select _to from relations where _to != '15' " \
    #             "and" \
    #             " _from in (select  _to from relations where _from = '15')"


    #result of IN operator
    array = mycol.find({"_from" : '15'},{"_to" : 1,"_id":0})
    list_IN = []
    for x in array :
        list_IN.append(x["_to"])
    record = mycol.find({ "$and" : [{"$or": [{ "_to " : { "$ne":  '15' }  },{ "_from" :  '15'}] },
                                    {"_from": {"$in": list_IN}}]},{"_to": 1 })


    for doc in record:
        print(doc)
    myclient.close()


def neighbors2data():
    myclient = create_connection()
    db = myclient.test
    mycol = db.relations

    #this is a sql query
    # neighbors2data_query = "select * from profiles where user_id::text IN (select _to from relations where _from = '20' union" \
    #                        " distinct select _to from relations where _to != '20' and _from IN" \
    #                        " (select  _to from relations where _from = '20'))"


    #result of IN operator
    array = mycol.find({"_from" : '20'},{"_to" : 1,"_id":0})
    list_IN = []
    for x in array :
        list_IN.append(x["_to"])
    innerQuery = mycol.find({ "$and" : [{"$or": [{ "_to " : { "$ne":  '20' }  },{ "_from" :  '20'}] },
                                    {"_from": {"$in": list_IN}}]},{"_to": 1 })
    list_inner_query = []
    for x in innerQuery :
        list_inner_query.append(x["_to"])
    #print(list_inner_query)

    mycol_profiles = db.profiles
    mainQuery = mycol_profiles.find({"user_id":{"$in" : list_inner_query}})

    #for doc in mainQuery:
     #   print(doc)

    myclient.close()

if __name__ == "__main__":
    #createDB()
    #createProfileCollection()
    #createRelationsCollection()
    #insertIntoProfilesCollection()
    #insertIntoRelationsCollection()
    #readProfilesCollection()
    #readRelationsCollection()
    #dropProfilesCollection()
    #dropRelationsCollection()
    dropDatabase()
    #singleRead()
    #singleWrite()
    #aggregate()
    #neighbors()
    #neighbors2()
    #neighbors2data()










