from flask import (
    Flask,
    request
)
from database import DB
from json import (
    dumps,
    loads
)
import configuration
from errors import errorResponse
from decorators import authorization_required
from time import time
from uuid import uuid4
from generators import generatePreviewData
from random import uniform
from s3 import S3

# SONGDB GENERATION
DATABASE = DB(db=configuration.DB_PATH)

SONGDB = {}

serverChangelist = 4294967295 / uniform(1.5, 1.9)
for SONG in DATABASE.getSongs():
    SONGDB[SONG['mapName']] = {
        "artist": SONG['artist'],
        'assets': {},
        'audioPreviewData': generatePreviewData(SONG['audioPreview']['BPM'],
                                                SONG['audioPreview']['Duration'],
                                                SONG['mapName']),
        'coachCount': SONG['coachCount'],
        'credits': SONG['credits'],
        'difficulty': SONG['difficulty'],
        'jdmAttributes': SONG['jdmAttributes'],
        'lyricsColor': SONG['lyricsColor'],
        'lyricsType': 0,
        'mainCoach': -1,
        'mapLength': SONG['mapLength'],
        'mapName': SONG['mapName'],
        "mapPreviewMpd": {
            "videoEncoding": {
                "vp8": f"<?xml version=\"1.0\"?>\r\n<MPD xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"urn:mpeg:DASH:schema:MPD:2011\" xsi:schemaLocation=\"urn:mpeg:DASH:schema:MPD:2011\" type=\"static\" mediaPresentationDuration=\"PT30S\" minBufferTime=\"PT1S\" profiles=\"urn:webm:dash:profile:webm-on-demand:2012\">\r\n\t<Period id=\"0\" start=\"PT0S\" duration=\"PT30S\">\r\n\t\t<AdaptationSet id=\"0\" mimeType=\"video/webm\" codecs=\"vp8\" lang=\"eng\" maxWidth=\"720\" maxHeight=\"370\" subsegmentAlignment=\"true\" subsegmentStartsWithSAP=\"1\" bitstreamSwitching=\"true\">\r\n\t\t\t<Representation id=\"0\" bandwidth=\"495888\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_LOW.vp8.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"588-1077\">\r\n\t\t\t\t\t<Initialization range=\"0-588\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"1\" bandwidth=\"1476873\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_MID.vp8.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"2\" bandwidth=\"2916702\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_HIGH.vp8.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"3\" bandwidth=\"4055531\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_ULTRA.vp8.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t</AdaptationSet>\r\n\t</Period>\r\n</MPD>\r\n",
                "vp9": f"<?xml version=\"1.0\"?>\r\n<MPD xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"urn:mpeg:DASH:schema:MPD:2011\" xsi:schemaLocation=\"urn:mpeg:DASH:schema:MPD:2011\" type=\"static\" mediaPresentationDuration=\"PT30S\" minBufferTime=\"PT1S\" profiles=\"urn:webm:dash:profile:webm-on-demand:2012\">\r\n\t<Period id=\"0\" start=\"PT0S\" duration=\"PT30S\">\r\n\t\t<AdaptationSet id=\"0\" mimeType=\"video/webm\" codecs=\"vp9\" lang=\"eng\" maxWidth=\"720\" maxHeight=\"370\" subsegmentAlignment=\"true\" subsegmentStartsWithSAP=\"1\" bitstreamSwitching=\"true\">\r\n\t\t\t<Representation id=\"0\" bandwidth=\"495888\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_LOW.vp9.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"588-1077\">\r\n\t\t\t\t\t<Initialization range=\"0-588\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"1\" bandwidth=\"1476873\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_MID.vp9.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"2\" bandwidth=\"2916702\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_HIGH.vp9.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t\t<Representation id=\"3\" bandwidth=\"4055531\">\r\n\t\t\t\t<BaseURL>jmcs://jd-contents/{SONG['mapName']}/{SONG['mapName']}_MapPreviewNoSoundCrop_ULTRA.vp9.webm</BaseURL>\r\n\t\t\t\t<SegmentBase indexRange=\"585-1075\">\r\n\t\t\t\t\t<Initialization range=\"0-585\" />\r\n\t\t\t\t</SegmentBase>\r\n\t\t\t</Representation>\r\n\t\t</AdaptationSet>\r\n\t</Period>\r\n</MPD>\r\n"
            }
        },
        "mode": 6,
        "originalJDVersion": SONG['originalJDVersion'],
        "packages": {
            "mapContent": f"{SONG['mapName']}_mapContent"
        },
        "parentMapName": SONG['parentMapName'],
        "skuIds": [],
        "songColors": SONG['songColors'],
        "status": 3,
        "sweatDifficulty": SONG['sweatDifficulty'],
        "tags": SONG['tags'],
        "title": SONG['title'],
        "urls": {},
        "serverChangelist": int(serverChangelist / uniform(1.5, 1.9))
    }

    STORAGE = S3()

    for key, val in configuration.ASSETS.items():
        val = val.format(SONG['mapName'])
            
        for object in STORAGE.getFiles():
            if val in object:
                SONGDB[SONG['mapName']]['assets'][key] = object
                break
        
    for key in configuration.URLS:
        key = key.format(SONG['mapName'])
        file = key.split("/")[-1]

        for object in STORAGE.getFiles():
            if file in object:
                SONGDB[SONG['mapName']]['urls'][key] = object
                break

del DATABASE

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

# Base URL(s): /songdb/v1/, /songdb/v2/, /sku-packages/v1/, /sku-packages/v2,
#              /questdb/v1/, /dance-machine/v1/
# Description: Map databases API

@APP.route("/songdb/v1/songs", methods=['GET'])
@APP.route("/songdb/v2/songs", methods=['GET'])
@authorization_required
def songdb():
    for xskuid in configuration.XSKU_IDS:
        if xskuid["code"] == request.headers['X-SkuId']: break

    CONTENT = SONGDB.copy()
    for KEY in CONTENT.keys():
        if KEY in xskuid['unavailableSongs']:
            del CONTENT[KEY]

    CONTENT = dumps(CONTENT)
    STATUS_CODE = 200
    HEADERS = {
        'Content-Type': 'application/json'
    }
    
    return CONTENT, STATUS_CODE, HEADERS

if __name__ == "__main__":
    APP.run()