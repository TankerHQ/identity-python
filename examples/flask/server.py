import flask
import path
import json

import tankersdk.usertoken

app = flask.Flask(__name__)
app.debug = True


# TODO: ensure config is stored in a secure place
def load_config():
    top_path = path.Path(".").abspath().parent
    trustchain_config = json.loads(top_path.joinpath("config-trustchain.json").text())
    app.config["TANKER"] = trustchain_config


load_config()


@app.route("/user_token")
def user_token():
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

    # TODO: retrieve the token of the current user if it exists
    token = None

    if not token:
        print("Creating new user token")
        tanker_config = app.config["TANKER"]
        trustchain_id = tanker_config["trustchainId"]
        trustchain_private_key = tanker_config["trustchainPrivateKey"]
        user_token = tankersdk.usertoken.generate_user_token(
            trustchain_id,
            trustchain_private_key,
            user_id
        )
        return user_token
