import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, url_for, render_template, request, session, jsonify, abort
from flask_dance.contrib.github import make_github_blueprint, github
from termcolor import colored

from py_tools import *

app = Flask(__name__)
app.secret_key = env_to_var("FLASK_SECRET_KEY")
github_blueprint = make_github_blueprint(client_id=env_to_var("GITHUB_CLIENT_ID"),
                                         client_secret=env_to_var("GITHUB_CLIENT_SECRET"))

app.register_blueprint(github_blueprint, url_prefix="/login")

cyan = lambda x: colored(x, "cyan")
green = lambda x: colored(x, "green")
red = lambda x: colored(x, "red")
yellow = lambda x: colored(x, "yellow")

@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    
    mongo = MongoDBHandler()
    
    if mongo.find_one("users", {"name": resp.json()['login']}) != None:
        seats = mongo.find_many("seating", {"username": resp.json()['login']})
        if seats != []:
            for seat in seats:
                del seat['_id']
            
            lst = []
            temp_lst = []
            count = 0
            for seat in seats:
                if count == 3:
                    count = 0
                    lst.append(temp_lst)
                    temp_lst = []
                temp_lst.append(seat['name'])
                count += 1
                
            if temp_lst:
                lst.append(temp_lst)
                
            seats = lst

            return render_template("index.html", seats=seats, exist_seats=1)

    student_names = [chr(i) for i in range(ord('A'), ord('A') + 9)]
    classroom = Classroom(student_names, width=3, height=3)
    seats = classroom.display_classroom()
    
    return render_template("index.html", seats=seats, exist_seats=0)
    
@app.route("/update-loc", methods=["POST"])
def update_loc():  
    resp = github.get("/user")

    data = request.get_json()
    
    if data['update'] == False:        
        mongo = MongoDBHandler()
        mongo.insert_one("seating", {"username": resp.json()['login'], "name": data['name'], "x": data['x'], "y": data['y']})
        
        mongo.close()
    else:       
        mongo = MongoDBHandler()
        mongo.update_one("seating", {"username": resp.json()['login'], "name": data['name']}, {"x": data['x'], "y": data['y']})
        mongo.close()
    
    return {}, 200

@app.route("/check-loc", methods=["POST"])
def check_loc():
    resp = github.get("/user")
    user = resp.json()['login']
    data = request.get_json()
    
    mongo = MongoDBHandler()
    seat = mongo.find_one("seating", {"username": user, "name": data['name']})
    mongo.close()
    
    
    return jsonify({"x": seat['x'], "y": seat['y']}), 200

if __name__ == "__main__":
    app.run(debug=True)