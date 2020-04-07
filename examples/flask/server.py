import flask
import json
import os

import tankersdk_identity

app = flask.Flask(__name__)
app.debug = True


# TODO: ensure config is stored in a secure place
def load_config():
    current_path = os.getcwd()
    json_path = os.path.join(current_path, "../config-app.json")
    with open(json_path) as stream:
        app_config = json.load(stream)
    app.config["TANKER"] = app_config


load_config()


@app.route("/identity")
def identity():
    request_args = flask.request.args
    user_id = request_args.get("user_id")
    if not user_id:
        return "Missing user_id", 400
    password = request_args.get("password")
    if not password:
        return "Missing password", 400

    # TODO: replace with your own logic to check a legitimate user is logged in
    #       and to retrieve his user id as needed by the Tanker SDK
    if password != "password" + user_id:
        return "Authentication error", 401

    print("New request:", user_id)

    # TODO: retrieve the identity of the current user if it exists
    identity = None

    if not identity:
        print("Creating new identity")
        tanker_config = app.config["TANKER"]
        app_id = tanker_config["appId"]
        app_secret = tanker_config["appSecret"]
        identity = tankersdk_identity.create_identity(app_id, app_secret, user_id)

    return identity
