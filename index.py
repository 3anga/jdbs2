from flask.helpers import flash
import configuration
from flask import Flask, request, abort
from sqlite3 import connect as db
from jwt import decode, encode
from time import time

DATABASE_CONN = db(configuration.DB_PATH)
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
    }

if __name__ == "__main__":
    APP.run()