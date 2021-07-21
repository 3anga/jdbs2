import sqlite3
from json import loads

class DB:
    def __init__(self, **kwargs):
        self.dbname = kwargs.get["db"].split("/")[-1].split(".")[0]
        self.session = sqlite3.connect(kwargs["db"])
    
    def __del__(self):
        self.session.close()

    def __str__(self):
        return "<Database {"+self.dbname+"}>"
    
    def getProfile(self, profileId = None):
        """
        Get profile from SQLite database
        """
        
        if profileId is None: return None

        cursor = self.session.cursor()
        cursor.execute(f'''SELECT * 
                           FROM profiles 
                           WHERE profileId={profileId};''')
        profileData = cursor.fetchone()
        cursor.close()

        if profileData is None: return None
        else: return {
            "avatar": profileData[0],
            "skin": profileData[1],
            "jdPoints": profileData[2],
            "progression": loads(profileData[3]),
            "history": loads(profileData[4]),
            "favorites": loads(profileData[5]),
            "unlockedAvatars": loads(profileData[6]),
            "unlockedSkins": loads(profileData[7]),
            "wdfRank": profileData[8],
            "stars": profileData[9],
            "unlocks": profileData[10],
            "songsPlayed": profileData[11],
            "name": profileData[12],
            "nickname": profileData[13],
            "platformId": profileData[14],
            "country": profileData[15],
            "scores": loads(profileData[16]),
            "language": profileData[17],
            "unlockedPortraitBorders": profileData[18],
            "portraitBorder": profileData[19],
            "syncVersions": loads(profileData[20]),
            "otherPids": loads(profileData[21]),
            "mapHistory": loads(profileData[22]),
            "profileId": profileId[23]
        }