import configuration
from flask import Flask, request, abort
from database import DB
from jwt import decode, encode
from time import time
from json import dumps

DATABASE = DB(db=configuration.DB_PATH)
APP = Flask(__name__)

#THIS WILL BE TEMPORARY OFFLINE 
#@APP.before_request
def before_request():
    try:
        if request.headers.get('User-Agent') in configuration.USER_AGENTS:
            decodedAuthorization = decode(request.headers.get('Authorization'), 
                                         configuration.PUBLIC_KEY,
                                         algorithm=configuration.JWT_ALGORITHM)
            if decodedAuthorization["banned"] == True or (time() *
                                                           1000) > (decodedAuthorization["serverTime"] + 
                                                                    decodedAuthorization["expiresIn"]):
                return abort(401)
            request.headers["Authorization"] = decodedAuthorization
        else:
            return abort(401)
    except Exception:
        return abort(401)

@APP.route('/profile/v2/profiles', methods=['GET', 'POST'])
def profiles():
    if request.method == 'GET':
        response = []
        for pid in request.args.get('profileIds').split(","):
            response.append(DATABASE.getProfile(pid))
        return dumps(response), 200, {"Content-Type": "application/json"}
    else:
        userId = request.headers["Authorization"]["userId"]
        if DATABASE.isProfileExists(userId) == True:
            DATABASE.updateProfile(userId, request.get_json())
        else:
            DATABASE.createProfile(userId, request.get_json())
        return 200

if __name__ == "__main__":
    APP.run()