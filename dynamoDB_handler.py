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


def add_item_to_user_table(regno, fullname, email, password, degree, contact, introduction, gpa, skills):
    response = UserTable.put_item(
        Item = {
            'regno'     : regno,
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
    
    # items = response['Items']
    # if items:
    #     fullname = items[0]['fullname']
        
    #     if password == items[0]['password']:
                
    #         return render_template("profile.html",fullname = fullname)
            
    #     errormsg = "Invalid Password!"
    #     return render_template("login.html", errormsg = errormsg)
    
    # else:
    #     errormsg2 = "Invalid E-mail!"
    #     return render_template("login.html", errormsg2 = errormsg2)
    
    return response

# def get_item_from_user_table(reg):
#     #
#     response = MovieTable.get_item(
#         Key = {
#             'id': id
#         },
#         AttributesToGet = [
#             'title','director'
#         ]
#     )
#     return response