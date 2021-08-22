from flask import Flask

from flask_pymongo import PyMongo   

from bson.json_util import dumps


from bson.objectid import ObjectId

from flask import jsonify, request

app = Flask(__name__)
app.secret_key = "secretkey"


app.config['MONGO_URI'] = "mongodb://localhost:27017/User"

mongo = PyMongo(app)


@app.route('/add',methods=['POST'])
def add_user():
	_json = request.json
	_name = _json['name']
	_address = _json['address']
	_contactno = _json['contact']
	_email = _json['email']
	
                   
	if _name and _address and _contactno and _email and request.method == 'POST':
		
		
		id = mongo.db.user.insert({'name':_name,'address':_address,'contact':_contactno,'email':_email})

		resp = jsonify("Contact added sucessfully")

		resp.status_code = 200

		return resp

	else:
			return not_found()



@app.route('/users')
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	return resp


@app.route('/user/<id>')
def user(id):
	user = mongo.db.user.find_one({'_id':ObjectId(id)})
	resp = dumps(user)
	return resp	



@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
	delete_user = mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify("Contact deleted successfully")

	resp.status_code = 200

	return resp	



@app.route('/update/<id>', methods =['PUT'])
def update(id):
	_id = id
	_json = request.json
	_name = _json['name']
	_address = _json['address']
	_contactno = _json['contact']
	_email = _json['email']
	


	if _name and _address and _contactno and _email and _id and request.method == 'PUT':
		

		mongo.db.user.update({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':_name,'address':_address,'contact':_contactno,'email':_email,}})
		resp = jsonify("Contact updated Successfully")
		resp.status_code = 200
		return resp
	else:
		return not_found()	



@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message':'Not Found' + request.url
	}

	resp = jsonify(message)

	resp.status_code = 404

	return resp



if __name__ =="__main__":  
	app.run(debug = True)  


  

