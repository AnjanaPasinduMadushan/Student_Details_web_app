import boto3

import key_config as keys

from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, render_template

dynamodb_client = boto3.client(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

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

UserTable = dynamodb_resource.Table('users')#getting the table


def check_regno(email):
    response = UserTable.query(
                KeyConditionExpression=Key('email').eq(email),
                ScanIndexForward=True,
                Limit=1
        )
    if 'Items' in response and len(response['Items']) > 0:
        print(response['Items'][0]['regno'])
        return response['Items'][0]['regno']
        
    else:
        print('this')
        return 0
        

def add_item_to_user_table(regno, fullname, email, password, degree, contact, introduction, gpa, skills):
    
    check = check_regno(email)
    response = UserTable.put_item(
        Item = {
            'regno'     : check+1,
            'fullname'  : fullname,
            'email' : email,
            'password'  : password,
            'degree'  : degree,
            'contact'  : contact,
            'introduction'  : introduction,
            'gpa'  : gpa,
            'skills'  : skills
        }
    )
    return response

def check_users(email, password):
    response = UserTable.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    
    return response

def get_item_from_Student_table(regno):
    #
    # response = UserTable.get_item(
    #     Key = {
    #         'regno': regno
    #     },
    #     AttributesToGet = [
    #         'regno', 'fullname', 'email', 'degree', 'contact', 'introduction', 'gpa', 'skills'
    #     ]
    # )
    
    response = UserTable.scan(
                FilterExpression='regno = :regno',
                ExpressionAttributeValues={':regno': regno }
        )
    return response
    
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