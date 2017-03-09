from flask import Flask 
from pymongo import MongoClient
 
app = Flask(__name__) 
mongo_object = MongoClient()
db = mongo_object['test']
collection = db['item']
 
@app.route('/') 
def pymongo_data_display():
    my_data = collection.find()
    return str([document for document in my_data]) 
 
if __name__ == '__main__': 
        app.run(host='0.0.0.0')
