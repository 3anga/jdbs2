# S3-compatible object storage connection settings

REGION_NAME = ''
ENDPOINT_URL = ''
ACCESS_ID = ''
SECRET_KEY = ''
BUCKET = ''

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

# ASSETS

ASSETS = {
    "banner_bkgImageUrl": "{0}_banner_bkg.tga.ckd",
    "coach1ImageUrl": "{0}_Coach_1.tga.ckd",
    "coach2ImageUrl": "{0}_Coach_2.tga.ckd",
    "coach3ImageUrl": "{0}_Coach_3.tga.ckd",
    "coach4ImageUrl": "{0}_Coach_4.tga.ckd",
    "coverImageUrl": "{0}_Cover_Generic.tga.ckd",
    "cover_1024ImageUrl": "{0}_Cover_1024.png",
    "cover_smallImageUrl": "{0}_Cover_Online.tga.ckd",
    "expandBkgImageUrl": "{0}_Cover_AlbumBkg.tga.ckd",
    "expandCoachImageUrl": "{0}_Cover_AlbumCoach.tga.ckd",
    "phoneCoach1ImageUrl": "{0}_Coach_1_Phone.png",
    "phoneCoach2ImageUrl": "{0}_Coach_2_Phone.png",
    "phoneCoach3ImageUrl": "{0}_Coach_3_Phone.png",
    "phoneCoach4ImageUrl": "{0}_Coach_4_Phone.png",
    "phoneCoverImageUrl": "{0}_Cover_Phone.jpg",
    "map_bkgImageUrl": "{0}_map_bkg.tga.ckd"
}
URLS = [
    "jmcs://jd-contents/{0}/{0}_AudioPreview.ogg",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_HIGH.vp8.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_HIGH.vp9.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_LOW.vp8.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_LOW.vp9.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_MID.vp8.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_MID.vp9.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_ULTRA.vp8.webm",
    "jmcs://jd-contents/{0}/{0}_MapPreviewNoSoundCrop_ULTRA.vp9.webm",
    "jmcs://jd-contents/{0}/{0}_ULTRA.webm",
    "jmcs://jd-contents/{0}/{0}_ULTRA.hd.webm",
    "jmcs://jd-contents/{0}/{0}_MID.webm",
    "jmcs://jd-contents/{0}/{0}_MID.hd.webm",
    "jmcs://jd-contents/{0}/{0}_LOW.webm",
    "jmcs://jd-contents/{0}/{0}_LOW.hd.webm",
    "jmcs://jd-contents/{0}/{0}_HIGH.webm",
    "jmcs://jd-contents/{0}/{0}_HIGH.hd.webm"
]
