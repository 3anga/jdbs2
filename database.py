import sqlite3, configuration
from json import loads, dumps
from time import time
from uuid import uuid4

class DB:
    def __init__(self, **kwargs):
        self.dbname = kwargs["db"].split("/")[-1].split(".")[0]
        self.session = sqlite3.connect(kwargs["db"], check_same_thread=False)
        self.cursor = self.session.cursor()

    def __str__(self):
        return "<Database {"+self.dbname+"}>"
    
    def getProfile(self, profileId = None):
        """
        Returns a profile from SQLite database
        """

        if profileId is None: return None
        with self.session:
            self.cursor.execute(f'''SELECT *
                                    FROM profiles;''')
            profiles = self.cursor.fetchall()
        for profile in profiles:
            if profile[-1].replace("'","") == profileId: return {
                "avatar": profile[0],
                "skin": profile[1],
                "jdPoints": profile[2],
                "progression": loads(profile[3].replace("'","")),
                "history": loads(profile[4].replace("'","")),
                "favorites": loads(profile[5].replace("'","")),
                "unlockedAvatars": loads(profile[6].replace("'","")),
                "unlockedSkins": loads(profile[7].replace("'","")),
                "wdfRank": profile[8],
                "stars": profile[9],
                "unlocks": profile[10],
                "songsPlayed": profile[11],
                "name": profile[12].replace("'",""),
                "nickname": profile[13].replace("'",""),
                "platformId": profile[14].replace("'",""),
                "country": profile[15],
                "scores": loads(profile[16].replace("'","")),
                "language": profile[17].replace("'",""),
                "unlockedPortraitBorders": loads(profile[18].replace("'","")),
                "portraitBorder": profile[19],
                "syncVersions": loads(profile[20].replace("'","")),
                "otherPids": loads(profile[21].replace("'","")),
                "mapHistory": loads(profile[22].replace("'","")),
                "profileId": profileId,
            }
        return None
    
    def isProfileExists(self, userId = None):
        """
        Checks profile for a existing.
        Returns a True or False
        """

        if userId is None: return False

        profileId = self.getUser(userId)["profileId"]

        with self.session:
            self.cursor.execute(f'''SELECT * 
                            FROM profiles;''')
            checks = self.cursor.fetchall()
        for check in checks:
            if check[-1].replace("'","") == profileId: return True
        return False
    
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

        with self.session:
            self.cursor.execute(f'''INSERT INTO profiles 
                            ({','.join(list(profile.keys()))})
                            VALUES ({values});''')
            self.session.commit()
    
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

        with self.session:
            self.cursor.execute(f'''UPDATE profiles
                            SET {setinfo}
                            WHERE profileId={profileId};''')
            self.session.commit()
    
    def getUser(self, userId = None):
        """
        Returns a user
        """

        if userId is None: return None

        with self.session:
            self.cursor.execute(f'''SELECT * 
                            FROM user
                            WHERE userId={userId};''')
            users = self.cursor.fetchone()

        for user in users:
            if user[0].replace("'","") == userId: return {
                "userId": userId,
                "profileId": user[1],
                "platformCode": user[2],
                user[2]: {
                    "name": user[3],
                    "email": user[4]
                },
                "discordId": user[5]
            }

        return None

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

        with self.session:
            self.cursor.execute(f'''INSERT INTO users
                            (userId,profileId,platformCode,name,email,discordId)
                            VALUES (?,?,?,?,?,?);''', (
                                userId,
                                str(uuid4()),
                                xskuid_["code"],
                                name,
                                email,
                                discordId
                            ))
            self.session.commit()
    
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

        with self.session:
            self.cursor.execute(f'''UPDATE users
                            SET {setinfo}
                            WHERE userId={userId};''')
            self.session.commit()