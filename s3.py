from boto3 import session
from configuration import (
    REGION_NAME,
    ENDPOINT_URL,
    ACCESS_ID,
    SECRET_KEY,
    BUCKET
)

class S3:
    def __init__(self):
        self.session = session.Session()
        self.client = self.session.client('s3',
                                          region_name=REGION_NAME,
                                          endpoint_url=f'https://{ENDPOINT_URL}',
                                          aws_access_key_id=ACCESS_ID,
                                          aws_secret_access_key=SECRET_KEY)

    def getFiles(self):
        response = self.client.list_objects_v2(Bucket=BUCKET)
        if 'Contents' not in response:
            return []
        
        result = []
        for key in response['Contents']:
            if "." in key['Key'] and key['Size'] > 0:
                result.append(f"https://{BUCKET}.{ENDPOINT_URL}/{key['Key']}")
        
        return result
