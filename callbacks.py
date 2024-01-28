import os
import subprocess
import requests
from zouti_utils.json import load_json

config = load_json("config.json")


def restart_viscon_support_app() -> None:
    git_pull("/home/zouti/VisconSupportApp")

    restart_service("viscon-support-app")

    send_notification("Git Notifier", "Restarted VisconSupportApp")


def restart_viscon_support_api() -> None:
    git_pull("/home/zouti/VisconSupportAPI")

    restart_service("viscon-support-api")

    send_notification("Git Notifier", "Restarted VisconSupportAPI")


def restart_tcp_file_server() -> None:
    git_pull("/home/zouti/TCPFileServer")

    restart_service("tcp-file-server")

    send_notification("Git Notifier", "Restarted TCPFileServer")


def restart_jonko_tracker_api() -> None:
    git_pull("/home/zouti/JonkoTrackerAPI")

    restart_service("jonko-tracker-api")

    send_notification("Git Notifier", "Restarted JonkoTrackerAPI")


def git_pull(directory: str) -> None:
    wd = os.getcwd()

    os.chdir(directory)

    p = subprocess.Popen(["git", "pull"])
    p.wait()

    os.chdir(wd)


def restart_service(service: str) -> int:
    return subprocess.call(["sh", "restart.sh", config["sudo_password"], service])


def send_notification(message: str, description: str):
    requests.post('https://api.mynotifier.app', {
        "apiKey": config["notifier_api_key"],
        "message": message,
        "description": description,
        "type": "success",
    })
