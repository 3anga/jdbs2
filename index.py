from flask import Flask, request
from database import DB
from json import dumps
import configuration 

APP = Flask(__name__)

@APP.route('/profile/v2/profiles', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        DATABASE = DB(db=configuration.DB_PATH)

        RESPONSE = []
        for PID in request.args.get('profileIds').split(","):
            RESPONSE.append(DATABASE.getProfile(PID))
        
        CONTENT = dumps(RESPONSE)
        STATUS_CODE = 200
        HEADERS = {
            'Content-Type': 'application/json'
        }

        del DATABASE

        return CONTENT, STATUS_CODE, HEADERS
    else:
        DATABASE = DB(db=configuration.DB_PATH)

        #TODO: change to real data
        USERID = 'd06b57e3-16a5-4828-b5a5-79de9e649841'

        BODY = request.get_json()
        XSKUID = request.headers.get('X-SkuId')

        if DATABASE.isProfileExists(USERID) == True:
            DATABASE.updateProfile(userId=USERID, profile=BODY)
        else:
            DATABASE.createProfile(userId=USERID, profile=BODY, xskuid=XSKUID)

        CONTENT = dumps([])
        STATUS_CODE = 200
        HEADERS = {
            'Content-Type': 'application/json'
        }

        del DATABASE

        return CONTENT, STATUS_CODE, HEADERS

if __name__ == "__main__":
    APP.run()