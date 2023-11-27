from flask import Flask, request
import hashlib
import hmac
from zouti_utils.json import load_json

from callbacks import (
    restart_viscon_support_app,
    restart_viscon_support_api,
    restart_tcp_file_server
)

app = Flask(__name__)

config = load_json("config.json")


def validate_signature(signature, payload):
    hash_obj = hmac.new(config["github_secret"].encode("utf-8"), msg=payload, digestmod=hashlib.sha256)
    expected_sig = "sha256=" + hash_obj.hexdigest()

    return hmac.compare_digest(expected_sig, signature)


@app.post("/")
def get_update():
    event = request.headers.get("X-Github-Event")
    signature = request.headers.get("X-Hub-Signature-256")

    if not validate_signature(signature, request.data):
        return "Invalid signature", 403

    if event != "push":
        return "Not a push event"

    data = request.json

    if data["repository"]["master_branch"] != data["ref"].split("/")[-1]:
        return "not master branch"

    match data["repository"]["name"]:
        case "VisconSupportApp":
            restart_viscon_support_app()
        case "VisconSupportAPI":
            restart_viscon_support_api()
        case "TCPFileServer":
            restart_tcp_file_server()

    return "ok"


if __name__ == "__main__":
    app.run("0.0.0.0", port=11113)
