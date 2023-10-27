import subprocess
import requests
from zouti_utils.json import load_json

config = load_json("config.json")


def restart_viscon_support_app():
    sudo_pass = config["sudo_password"]
    subprocess.run(
        ["echo", f"'{sudo_pass}'", "|", "sudo", "-S", "systemctl", "restart", "viscon-support-app"],
        shell=True, check=True
    )
    send_notification("Git Notifier", "Restarted VisconSupportApp")


def restart_viscon_support_api():
    sudo_pass = config["sudo_password"]
    subprocess.run(
        ["echo", f"'{sudo_pass}'", "|", "sudo", "-S", "systemctl", "restart", "viscon-support-app"],
        shell=True, check=True
    )
    send_notification("Git Notifier", "Restarted VisconSupportAPI")


def send_notification(message: str, description: str):
    requests.post('https://api.mynotifier.app', {
        "apiKey": config["notifier_api_key"],
        "message": message,
        "description": description,
        "type": "success",
    })
