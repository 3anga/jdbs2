from json import dumps
from uuid import uuid4

def errorResponse(msg="Unknown error", code=500):
    CONTENT = dumps({
        'statusCode': code,
        'message': msg,
        'requestId': uuid4().hex
    })
    STATUS_CODE = code
    HEADERS = {
        'status': 'bad',
        'Content-Type': 'application/json'
    }
    
    return CONTENT, STATUS_CODE, HEADERS