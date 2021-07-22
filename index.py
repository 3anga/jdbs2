from flask import Flask, request
from database import DB
from json import dumps
import configuration
from errors import errorResponse
from decorators import authorization_required

APP = Flask(__name__)

@APP.route('/profile/v2/profiles', methods=['GET', 'POST'])
@authorization_required
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

        USERID = request.authorization["userId"]

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