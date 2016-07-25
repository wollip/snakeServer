from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json
import requests
import json

app = Flask(__name__)
#api = Api(app)

#class ID(Resource): 
#    def get(self):

#        with open('reply.json', 'w') as outfile:
#            json_stuff = json.dumps(direction)
#            json.dump(json_stuff, outfile)

#        return json_stuff


#api.add_resource(ID, '/height/<string:height>/weight/<string:weight>/city/<string:city>/state/<string:state>')
@app.route('/users/<username>')
def showUserName(username):
	return 'User {}'.format(username)

@app.route('/test', methods = ['GET', 'POST'])
def upload_file():
	print('hello')
	if request.method == 'POST':
		f = request.files['POST']
		f.save('whatever.txt')
		print('i saved something')

if __name__ == '__main__':
    app.run()