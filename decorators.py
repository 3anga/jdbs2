import jwt
from flask import request
from functools import wraps
from errors import errorResponse
from time import time
from configuration import (
    PUBLIC_KEY, 
    JWT_ALGORITHM
)

def authorization_required(function):
    @wraps(function)

    def wrapper(*args, **kwargs):
        try:
            request.authorization = jwt.decode(
                request.headers.get('Authorization').split(" ")[-1],
                PUBLIC_KEY,
                JWT_ALGORITHM
            )

            expiration = (
                request.authorization["serverTime"] + 
                request.authorization["expiresIn"]
            )
            if int(time() * 1000) > expiration:
                return errorResponse(
                    "Expired authorization", 
                    401
                )
            
            return function(*args, **kwargs)
        except Exception as err:
            return errorResponse(msg=err.args[0],code=500)
    
    return wrapper