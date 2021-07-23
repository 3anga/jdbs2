from flask import Flask, request
from database import DB
from json import dumps, loads
import configuration
from errors import errorResponse
from decorators import authorization_required
from time import time
from uuid import uuid4

APP = Flask(__name__)

# Base URL(s): /profile/v2/
# Description: Profile API. This uses database.

@APP.route('/profile/v2/profiles', methods=['GET', 'POST'])
@authorization_required
def profiles():
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

        CONTENT = dumps({})
        STATUS_CODE = 200
        HEADERS = {
            'Content-Type': 'application/json'
        }

        del DATABASE

        return CONTENT, STATUS_CODE, HEADERS

@APP.route("/profile/v2/map-ended", methods=['POST'])
@authorization_required
def map_ended():
    DATABASE = DB(db=configuration.DB_PATH)

    USERID = request.authorization["userId"]

    XSKUID = request.headers.get('X-SkuId')
    BODY = request.get_json(silent=True)

    PROFILE = DATABASE.getProfile(USERID)

    for SCORE in BODY:
        PROFILE["mapHistory"]["classic"].append({
            'mapName': SCORE['mapName'],
            'score': SCORE['score'],
            'timestamp': int(time() * 1000)
        })

    DATABASE.updateProfile(USERID, 
                           { 'mapHistory': PROFILE["mapHistory"] },
                           XSKUID)

    del DATABASE

    CONTENT = dumps({})
    STATUS_CODE = 200
    HEADERS = {
        'Content-Type': 'application/json'
    }

    return CONTENT, STATUS_CODE, HEADERS

# TODO: Reverse-engineering this request
@APP.route("/profile/v2/filter-players", methods=['POST'])
@authorization_required
def filter_players():
    CONTENT = dumps([
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4())
    ])
    STATUS_CODE = 200
    HEADERS = {
        'Content-Type': 'application/json'
    }

    return CONTENT, STATUS_CODE, HEADERS

@APP.route("/profile/v2/favorites/maps/<MAP>", methods=['PUT', 'DELETE'])
@authorization_required
def favorite(MAP):
    DATABASE = DB(db=configuration.DB_PATH)

    USERID = request.authorization["userId"]
    XSKUID = request.headers.get('X-SkuId')

    PROFILE = DATABASE.getProfile(USERID)

    if request.method == 'PUT':
        if MAP in PROFILE["favorites"] == True:
            return errorResponse("Map is already in favorites", 500)
        PROFILE["favorites"].append(MAP)
    else:
        if MAP in PROFILE["favorites"] == False:
            return errorResponse("Map is not in favorites", 500)
        INDEX = 0
        for FAVORITE in PROFILE["favorites"]:
            if FAVORITE == MAP:
                PROFILE["favorites"].pop(INDEX)
                break
            else: INDEX += 1
    
    DATABASE.updateProfile(USERID, 
                           { 'favorites': PROFILE["favorites"] },
                           XSKUID)

    del DATABASE

    CONTENT = dumps({})
    STATUS_CODE = 200
    HEADERS = {
        'Content-Type': 'application/json'
    }

    return CONTENT, STATUS_CODE, HEADERS

if __name__ == "__main__":
    APP.run()