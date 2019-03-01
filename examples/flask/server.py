import flask
import json
import os

import tanker_identity

app = flask.Flask(__name__)
app.debug = True


# TODO: ensure config is stored in a secure place
def load_config():
    current_path = os.getcwd()
    json_path = os.path.join(current_path, "../config-trustchain.json")
    with open(json_path) as stream:
        trustchain_config = json.load(stream)
    app.config["TANKER"] = trustchain_config


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
        trustchain_id = tanker_config["trustchainId"]
        trustchain_private_key = tanker_config["trustchainPrivateKey"]
        identity = tanker_identity.identity.create_identity(
            trustchain_id,
            trustchain_private_key,
            user_id
        )

    return identity
