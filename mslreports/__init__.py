import requests

from . import config

def connect():
    session = requests.Session()
    session.auth = (config.username, config.password)
    try:
        session.get("https://mslreports.jpl.nasa.gov/")
        config.session = session
    except requests.HTTPError as exc:
        raise Exception(
            "Could not connect to MSL Reports. Check credentials and VPN connection."
        ) from exc
