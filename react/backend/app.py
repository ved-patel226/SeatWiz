import os

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from flask_cors import CORS, cross_origin

from py_tools import *

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)


app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)

load_dotenv()

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_SECRET_KEY = os.environ["GOOGLE_SECRET_KEY"]


@app.route("/", methods=["GET"])
def hello_world():
    return "hello world"


@app.route("/google_login", methods=["POST"])
def login():
    auth_code = request.get_json()["code"]

    data = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_SECRET_KEY,
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }

    response = requests.post("https://oauth2.googleapis.com/token", data=data).json()
    headers = {"Authorization": f'Bearer {response["access_token"]}'}
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", headers=headers
    ).json()

    jwt_token = create_access_token(identity=user_info["email"])
    response = jsonify(user=user_info)
    response.set_cookie("access_token_cookie", value=jwt_token, secure=True)

    return response, 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():

    jwt_token = request.cookies.get("access_token_cookie")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/is_authenticated", methods=["GET"])
@jwt_required(optional=True)
@cross_origin(origins=["http://localhost:5173"])
def is_authenticated():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(authenticated=True, user=current_user), 200
    else:
        return jsonify(authenticated=False), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
