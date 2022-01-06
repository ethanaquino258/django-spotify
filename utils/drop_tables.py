import boto3


ddb = boto3.client('dynamodb', endpoint_url='http://localhost:3000')

response = ddb.list_tables()

for table in response['TableNames']:
    ddb.delete_table(TableName=table)

print(ddb.list_tables())
