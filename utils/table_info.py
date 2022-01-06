import boto3
from botocore.exceptions import ClientError
from dynamodb_json import json_util as json
import pandas as pd

ddb = boto3.client('dynamodb', endpoint_url='http://localhost:3000')

print(ddb.list_tables())

# print(ddb.scan(TableName='aquinyo_library'))

result = ddb.scan(TableName='aquinyo_library')
# print(json.loads(result['Items']))

# df = pd.DataFrame(json.loads(result['Items']))

# print(df[['genres', 'uri']])

# for entry in df.iterrows():
#     if 'folk' in entry[1]['genres']:
#         print(entry[1]['uri'])

# print(result)

# genres = ddb.scan(TableName='aquinyo_genres')
# print(genres)
