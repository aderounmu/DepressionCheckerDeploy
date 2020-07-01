"""
This is the flask entry for the react applicaton 
"""
from flask import Flask
#from flask_cors import CORS
from flask import render_template
from flask import jsonify
from services import services
from services import noUser
import time

app = Flask(__name__,static_folder='./build',static_url_path="/")
# CORS(app)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv



@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(error):
	return app.send_static_file('index.html')

@app.route('/')
def home():
	return app.send_static_file('index.html')



@app.route('/api/tweets/<username>')
def tweets(username):
	startTime = time.time()
	try:
		user = str(username) #make su
		myservice = services(username=user) 
		myservice.getTweets()
	except(noUser):
		raise InvalidUsage('This user doesnt exist or has no tweets',status_code=403)
	except Exception as e:
		raise InvalidUsage('Something Went wrong, Check your internet Connection')
	else:
		myservice.predict()
		endTime = time.time()
		length = len(myservice.response())
		username= myservice.username
		return {"meta": {"duration":'{} secs'.format(endTime-startTime),"length":length , "username" : username}, "data" : myservice.response()}

@app.route('/api/tweet/<text>')
def tweet(text): 
	service = services(text=text)
	service.predict()
	return service.response()
@app.route('/api/tweet/<username>/latest')
def lastest(username):
	return {"data":'Welcome {}'.format(username)}




if __name__ == '__main__':
	app.run(debug=False)