import sqlite3, configuration
from json import loads, dumps
from time import time
from uuid import uuid4

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
        Returns a profile from SQLite database
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
    
    def isProfileExists(self, userId = None):
        """
        Checks profile for a existing.
        Returns a True or False
        """

        if userId is None: return False

        profileId = self.getUser(userId)["profileId"]

        cursor = self.session.cursor()
        cursor.execute(f'''SELECT * 
                           FROM profiles 
                           WHERE profileId={profileId};''')
        check = cursor.fetchone()
        cursor.close()

        if check is None: return False
        else: return True
    
    def createProfile(self, userId = None, profile = None, xskuid = None):
        """
        Creates a profile using userId
        """

        if userId or profile or xskuid is None: return None

        profile["profileId"] = self.getUser(userId)["profileId"]

        for xskuid_ in configuration.XSKU_IDS:
            if xskuid_["code"] == xskuid: break

        profile["syncVersions"] = {
            xskuid_["gameVersion"]: {
                'version': 0,
                'timestamp': int(time() * 1000)
            }
        }
        profile["platformId"] = xskuid_["platformId"]

        values = str()
        lastValue = list(profile.values())[-1]
        for value in profile.values():
            if type(value) == str:
                values += f"'{value}'"
            elif type(value) == dict or list:
                values += f"'{dumps(value)}'"
            else:
                values += f"'{str(value)}'"
            
            if value != lastValue: values += ","

        cursor = self.session.cursor()
        cursor.execute(f'''INSERT INTO profiles 
                           ({','.join(list(profile.keys()))})
                           VALUES ({values});''')
        response = cursor.fetchone()
        cursor.close()

        return response
    
    def updateProfile(self, userId=None, profile=None):
        """
        Updates a profile in SQLite database
        """

        if userId or profile is None: return

        profileId = self.getUser(userId)["profileId"]

        setinfo = str()
        lastValue = list(profile.values())[-1]
        for key, value in profile.items():
            setinfo += f"{key}="

            if type(value) == str:
                setinfo += f"'{value}'"
            elif type(value) == dict or list:
                setinfo += f"'{dumps(value)}'"
            else:
                setinfo += f"'{str(value)}'"

            if value != lastValue: setinfo += ","

        cursor = self.session.cursor()
        cursor.execute(f'''UPDATE profiles
                           SET {setinfo}
                           WHERE profileId={profileId};''')
        response = cursor.fetchone()
        cursor.close()

        return response
    
    def getUser(self, userId = None):
        """
        Returns a user
        """

        if userId is None: return None

        cursor = self.session.cursor()
        cursor.execute(f'''SELECT * 
                           FROM user
                           WHERE userId={userId};''')
        userData = cursor.fetchone()
        cursor.close()

        if userData is None: return None
        else: return {
            "userId": userData[0],
            "profileId": userData[1],
            "platformCode": userData[2],
            userData[2]: {
                "name": userData[3],
                "email": userData[4]
            },
            "discordId": userData[5]
        }

    def createUser(self, userId = None,
                   name = None,
                   email = None,
                   discordId = None,
                   xskuid = None):
        """
        Creates a user
        """

        if userId or name or discordId or xskuid is None: return None

        for xskuid_ in configuration.XSKU_IDS:
            if xskuid_["code"] == xskuid: break

        cursor = self.session.cursor()
        cursor.execute(f'''INSERT INTO users
                           (userId,profileId,platformCode,name,email,discordId)
                           VALUES (?,?,?,?,?,?);''', (
                               userId,
                               str(uuid4()),
                               xskuid_["code"],
                               name,
                               email,
                               discordId
                           ))
        response = cursor.fetchone()
        cursor.close()

        return response
    
    def updateUser(self, userId = None, **kwargs):
        """
        Update a user
        """

        setinfo = str()
        lastValue = list(kwargs.values())[-1]
        for key, value in kwargs.items():
            setinfo += f"{key}="

            if type(value) == str:
                setinfo += f"'{value}'"
            elif type(value) == dict or list:
                setinfo += f"'{dumps(value)}'"
            else:
                setinfo += f"'{str(value)}'"

            if value != lastValue: setinfo += ","

        cursor = self.session.cursor()
        cursor.execute(f'''UPDATE users
                           SET {setinfo}
                           WHERE userId={userId};''')
        response = cursor.fetchone()
        cursor.close()

        return response