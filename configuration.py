# S3-compatible object storage connection settings

REGION_NAME = ''
ENDPOINT_URL = ''
ACCESS_ID = ''
SECRET_KEY = ''

# Key
# You can generate this with ssh-keygen or this website (http://travistidwell.com/jsencrypt/demo)

PRIVATE_KEY = b''''''
PUBLIC_KEY = b''''''

# JWT settings

JWT_ALGORITHM = "RS256"

# WDF Rooms

WDF_ROOMS = [{
    "roomCode": "main",
    "bots": True,
    "mode": {
        "tournaments": True,
        "vote": True,
        "ugc": False
    }
}]

# X-Sku IDs

XSKU_IDS = [{
    "code": "jd2017-pc-ww",
    "platformCode": "uplay",
    "platformId": "uplay",
    # if gameVersions or unavailableSongs will be true, 
    # then this will be avaliable for every countries or will be unavaliable every song in this xskuid 
    "unavailableSongs": [
        "Placeholder"
    ],
    "gameVersions": [
        2017
    ],
    "active": True,
    "dev": False,
    "default": False
}]

# Special songs 

SPECIAL_SONGS = [{
    "mapName": "Placeholder",
    # if gameVersions or countries will be true, then this will be avaliable for every countries or games
    "onlyAvailable": {
        "countries": [],
        "gameVersions": True
    }
}]

# Database

DB_PATH = ''

# User-Agents

USER_AGENTS = []
