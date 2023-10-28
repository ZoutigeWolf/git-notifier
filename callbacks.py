import os
import subprocess
import requests
from zouti_utils.json import load_json

config = load_json("config.json")


def restart_viscon_support_app():
    wd = os.getcwd()

    os.chdir("/home/zouti/VisconSupportApp")

    p = subprocess.Popen(["git", "pull"])
    p.wait()

    os.chdir(wd)

    subprocess.call(["./restart.sh", config["sudo_password"], "viscon-support-app"])

    send_notification("Git Notifier", "Restarted VisconSupportApp")


def restart_viscon_support_api():
    wd = os.getcwd()

    os.chdir("/home/zouti/VisconSupportAPI")

    p = subprocess.Popen(["git", "pull"])
    p.wait()

    os.chdir(wd)

    subprocess.call(["./restart.sh", config["sudo_password"], "viscon-support-api"])

    send_notification("Git Notifier", "Restarted VisconSupportAPI")


def send_notification(message: str, description: str):
    requests.post('https://api.mynotifier.app', {
        "apiKey": config["notifier_api_key"],
        "message": message,
        "description": description,
        "type": "success",
    })
