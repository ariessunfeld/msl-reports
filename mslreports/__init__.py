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


def enable_uploading():
    driver = _create_headless_driver()
    config.driver = driver


def _create_headless_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions

    drivers = [
        {
            'driver': webdriver.Chrome,
            'options': ChromeOptions(),
            'name': 'Chrome'
        },
        {
            'driver': webdriver.Firefox,
            'options': FirefoxOptions(),
            'name': 'Firefox'
        },
        {
            'driver': webdriver.Edge,
            'options': EdgeOptions(),
            'name': 'Edge'
        }
    ]

    for browser in drivers:
        try:
            browser['options'].add_argument('--headless')
            driver = browser['driver'](options=browser['options'])
            config.logger.info(f"Using {browser['name']} in headless mode.")
            return driver
        except Exception as err:
            config.logger.info(f"Failed to start {browser['name']} driver. Error: {err}")
            continue

    fail_msg = "No supported browsers found. Please install Chrome, Edge, or Firefox."
    config.logger.critical(fail_msg)
    raise Exception(fail_msg)
