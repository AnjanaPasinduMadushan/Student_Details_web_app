import boto3

import key_config as keys

from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, render_template

dynamodb_client = boto3.client(
    'dynamodb',
    # aws_access_key_id     = keys.ACCESS_KEY_ID,
    # aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    # aws_access_key_id     = keys.ACCESS_KEY_ID,
    # aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

# function for creating the table
def create_table():
   table = dynamodb_resource.create_table(
       TableName = 'users', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'email',
               'KeyType'      : 'HASH' #RANGE = sort key, HASH = partition key
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'email', # Name of the attribute
               'AttributeType': 'S'   # N = Number (B= Binary, S = String)
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table

UserTable = dynamodb_resource.Table('users')#gobal variable for getting the table

# function for adding new students to table
def add_item_to_user_table(data):
    
    response_email = UserTable.query(
                KeyConditionExpression=Key('email').eq(data['email'])
        )
        
    response_id = get_item_from_Student_table(data['regno'])
    
    if response_id['Items']:
        existing_id = response_id['Items'][0]['regno']
        if existing_id == data['regno']:
            return {'error': "Student already registered with this registratioin number"}
    
    if response_email['Items']:
        existing_email = response_email['Items'][0]['email']
        if existing_email == data['email']:
            return {'error': "This email already exists"}
    
    response = UserTable.put_item(
        Item = {
            'regno'     : data['regno'],
            'fullname'  : data['fullname'],
            'email' : data['email'],
            'password'  : data['password'],
            'degree'  : data['degree'],
            'contact'  : data['contact'],
            'introduction'  : data['introduction'],
            'gpa'  : data['gpa'],
            'skills'  : data['skills'],
            'image_url': 'null'
        }
    )
    return response

# checking users email and password when logging to the system
# query action is used
def check_users(email, password):
    response = UserTable.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    
    return response

# function for getting student details using relevent registration number
# scan action is used
def get_item_from_Student_table(regno):
    
    response = UserTable.scan(
                FilterExpression='regno = :regno',
                ExpressionAttributeValues={':regno': regno }
        )
    return response

# function for update user details
def update_item_from_Student_table(data):
    
    response = UserTable.update_item(
        Key = {
               'email': data['email']
            },
            AttributeUpdates={
                
                'regno': {
                   'Value'  : data['regno'],
                   'Action' : 'PUT' 
                },
                'fullname': {
                   'Value'  : data['fullname'],
                   'Action' : 'PUT'
                },
                # 'email': {
                #   'Value'  : data['email'],
                #   'Action' : 'PUT' 
                # },
                'degree': {
                   'Value'  : data['degree'],
                   'Action' : 'PUT'
                },
                'contact': {
                   'Value'  : data['contact'],
                   'Action' : 'PUT'
                },
                'introduction': {
                   'Value'  : data['introduction'],
                   'Action' : 'PUT' 
                },
                'gpa': {
                   'Value'  : data['gpa'],
                   'Action' : 'PUT'
                },
                'skills': {
                   'Value'  : data['skills'],
                   'Action' : 'PUT' 
                }
                
            },
            
            ReturnValues = "UPDATED_NEW"  # returns the new updated value
    )
        
    return response
    
    
def update_image_url(email, object_url):
    response = UserTable.update_item(
        Key={
            'email': email
        },
        AttributeUpdates={
            'image_url': {
                'Value': object_url,
                'Action': 'PUT'
            }
        },
        ReturnValues="UPDATED_NEW"  # returns the new updated value
    )
    return response
