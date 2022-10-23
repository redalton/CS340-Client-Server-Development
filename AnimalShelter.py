from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads

class AnimalShelter(object):
    
    def __init__(self, username, password):
        #Using the fix suggested by Shaun Ryan which worked wonders!
        self.client = MongoClient('localhost:47163') #connect to the mongo service at port 47163
        self.database = self.client.AAC #set the database to AAC
        self.database.authenticate(username, password, source='AAC') #Authenticate using the supplied username and password passed in the parameter
        
    #method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            add = self.database.animals.insert_one(data) #if data is not empty, insert one into the database
            if add != 0:
                return True #if one item is added, return true
            else:
                return False #if no items were added, return false
        else:
            raise Exception("nothing to save, because data parameter is empty") #If there is no data passed in, throw an expection
            
    #method to implement the R in CRUD
    def read(self, searchDict):
        results = self.database.animals.find(searchDict) #Search the database for the given key and value pair passed in the parameters
        if results != 0:
            return(results) #if there are results, return them
        else:
            raise Exception("No values found with that pair") #if no items are found, throw an exception

    def readAll(self, searchDict):
        results = self.database.animals.find(searchDict,{"_id":False})
        return results
            
    #method to implement U in CRUD
    def update(self, searchDict, updateDict):
        if searchDict is not None:
            results = self.database.animals.update_one(searchDict, updateDict) #use update one to update the first item found by the search criteria supplied by searchDict
            jsonResult = dumps(results.raw_result) #convert the results to JSON and return
            return jsonResult
        else:
            raise Exception("Must include a search parameter") #if there are no search parameters, return an error
            
    #method to implement D in CRUD
    def delete(self, searchDict):
        if searchDict is not None:
            result = self.database.animals.delete_one(searchDict) #use delete_one to delete the first value found by the searchDict criteria
            jsonResult = dumps(results.raw_result) #convert to JSON and return
            return jsonResult
        else:
            raise Exception("Must include a valid search parameter") #if there are no search parameters, return an error