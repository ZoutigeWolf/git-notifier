from flask import Flask, request

from callbacks import restart_viscon_support_app, restart_viscon_support_api

app = Flask(__name__)


@app.post("/")
def get_update():
    event = request.headers.get("X-Github-Event")

    if event != "push":
        return "ok"

    data = request.json

    if data["repository"]["master_branch"] != data["ref"].split("/")[-1]:
        return "ok"

    match data["repository"]["name"]:
        case "VisconSupportApp":
            restart_viscon_support_app()
        case "VisconSupportAPI":
            restart_viscon_support_api()

    return "ok"


if __name__ == "__main__":
    app.run(port=11113)
