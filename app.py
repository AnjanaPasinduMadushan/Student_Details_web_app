from flask import Flask, request, render_template

import boto3

import dynamoDB_handler as dynamodb


app = Flask(__name__)

@app.route('/')#decorator for home page
def root_route():
    # dynamodb.create_table()
    # return 'Table Created'
    return render_template("sign_up.html")
    
@app.route('/login')
def login():    
    return render_template('login.html')
    

@app.route('/sign_up', methods=['POST'])
def add_user():
    data = request.form.to_dict()
    response = dynamodb.add_item_to_user_table(int(data['regno']), data['fullname'], data['email'],
     data['password'], data['degree'], data['contact'], data['introduction'], data['gpa'], data['skills'])
  
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        msg = "Registration Complete. Please Login to your account !"
        return render_template('login.html', msg = msg)

    return {  
        'msg': 'Some error occcured',
        'response': response
    }

@app.route('/check', methods=['POST'])
def check_user():
    data = request.form.to_dict()
    response = dynamodb.check_users(data['email'], data['password'])
    items = response['Items']
    if items:
        
        #fullname = items['fullname']
        item = items[0]
        
        if data['password'] == item['password']:
                
            return render_template("profile.html", item = item)
            
        errormsg = "Invalid Password!"
        return render_template("login.html", errormsg = errormsg)
    
    else:
        errormsg2 = "Invalid E-mail!"
        return render_template("login.html", errormsg2 = errormsg2)
        
    
@app.route('/profile/<int:rNo>', methods=["GET"])
def get_movie(rNo):
    response = dynamodb.get_item_from_Student_table(rNo)
    
    #return response
    users = response['Items'][0]
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
    
        if users:
            return users
        
        return { 'msg' : 'User not found!' }
    
    return {
        'msg': 'Some error occured',
        'response': response
    }
    


#define port and host
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')