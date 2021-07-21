from flask.helpers import flash
import configuration
from flask import Flask, request, abort
from database import db
from jwt import decode, encode
from time import time
from json import dumps

DATABASE = db(configuration.DB_PATH)
APP = Flask(__name__)

@APP.before_request
def before_request():
    try:
        decodedAuthorization = decode(request.headers.get('Authorization'), 
                                      configuration.PUBLIC_KEY,
                                      algorithm=configuration.JWT_ALGORITHM)
        if decodedAuthorization["banned"] == True or (time() *
                                                      1000) > (decodedAuthorization["serverTime"] + 
                                                               decodedAuthorization["expiresIn"]):
            return abort(401)
    except Exception:
        return abort(401)

@APP.route('/', methods=['GET'])
def index():
    return {
        "success": True
    }, 200, {
        "Status": "Good"
    }

@APP.route('/profile/v2/profiles', methods=['GET', 'POST'])
def profiles():
    if request.method == 'GET':
        response = []
        ##needs to make db system
        return dumps(response), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    APP.run()