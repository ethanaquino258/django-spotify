import boto3
from botocore.exceptions import ClientError

ddb = boto3.client('dynamodb', endpoint_url='http://localhost:3000')

try:
    response = ddb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N',
            },
            # {
            #     'AttributeName': 'name',
            #     'AttributeType': 'S',
            # },
            # {
            #     'AttributeName': 'artists',
            #     'AttributeType': 'S',
            # },
            # {
            #     'AttributeName': 'genres',
            #     'AttributeType': 'S',
            # },
            # {
            #     'AttributeName': 'uri',
            #     'AttributeType': 'S',
            # },
            # {
            #     'AttributeName': 'time_added',
            #     'AttributeType': 'S',
            # },
            # {
            #     'AttributeName': 'entry_time',
            #     'AttributeType': 'S',
            # },
        ],
        TableName=f'aquinyo_library',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            # {
            #     'AttributeName': 'name',
            #     'KeyType': 'HASH'
            # },
            # {
            #     'AttributeName': 'artists',
            #     'KeyType': 'RANGE'
            # },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        }
    )
    print(f'SONG TABLE CREATION:\n{response}\n')

    response2 = ddb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
            # {
            #     'AttributeName': 'genre',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'occurences',
            #     'AttributeType': 'N'
            # },
        ],
        TableName=f'aquinyo_genres',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        }
    )

    print(f'GENRE TABLE CREATION:\n{response2}\n')
except ClientError as e:
    print(e)

print(ddb.list_tables())
