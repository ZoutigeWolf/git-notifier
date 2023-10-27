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

    sudo_pass = config["sudo_password"]

    p = subprocess.Popen(["echo", f"\"{sudo_pass}\"", "|", "sudo", "-S", "systemctl", "restart", "viscon-support-app"])
    p.wait()

    os.chdir(wd)

    send_notification("Git Notifier", "Restarted VisconSupportApp")


def restart_viscon_support_api():
    wd = os.getcwd()

    os.chdir("/home/zouti/VisconSupportAPI")

    p = subprocess.Popen(["git", "pull"])
    p.wait()

    sudo_pass = config["sudo_password"]

    p = subprocess.Popen(["echo", f"\"{sudo_pass}\"", "|", "sudo", "-S", "systemctl", "restart", "viscon-support-api"])
    p.wait()

    os.chdir(wd)

    send_notification("Git Notifier", "Restarted VisconSupportAPI")


def send_notification(message: str, description: str):
    requests.post('https://api.mynotifier.app', {
        "apiKey": config["notifier_api_key"],
        "message": message,
        "description": description,
        "type": "success",
    })
