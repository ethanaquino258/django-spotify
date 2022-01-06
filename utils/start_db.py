import os

os.system('cd ../../dynamodb_local_latest')
os.system(
    'java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -port 3000')

print('running')
