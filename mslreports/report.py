"""Base class for MSLReports `Report` objects"""

import os
import json
from pathlib import Path

import requests

from .constants import TOPIC_URL_TO_FUNC_NAME
from . import config

class Report:
    """Represents a Report from MSL Reports
    Used as a base class for other reports,
    like ChemCamSPDLReport, ChemCamSPULReport, etc.

    Attributes:
        sol (Martian solar day for this report)
        role (E.g., ChemCam Science PDL, or DAN PUL, etc)
        topics (List of page subsections that contain text)
        summary (Summary text)
        contacts (Contacts text)
        email (email parsed from Contacts text)

    Additional Attributes:
        When initialized, whatever topics are in the `topics` argument will try to
        be converted into attributes for the report.

        Examples:

            engineering_requests
            detailed_report
            anomalies_and_concerns
            ...

        The specific additional attributes present depend on the Role of the report

    """
    def __init__(self, sol, role, topics, attachments):
        self.sol = sol
        self.role = role.NAME
        self.description = role.DESCRIPTION
        self.subsystem = role.SUBSYSTEM_CODE
        self._role = role
        self._topics = topics
        self._attachments = attachments # Attachments and their full URLs
        self.attachments = [a for a in self._attachments] # List of attachments
        self.topics = []
        self._init_defaults()

        for topic_key, topic_content in self._topics.items():
            pythonic_name = TOPIC_URL_TO_FUNC_NAME.get(topic_key, None)
            if pythonic_name:
                setattr(self, pythonic_name, topic_content)
                self.topics.append(pythonic_name)

        self._parse_email()

    def download_attachment(self, attachment, local_location='.', replace=False):
        """Downloads attachment by looking up path with self._attachments.get(attachment)

        Uses Pathlib and os for local_location, which can be either a directory or a filepath
        Raises error if file already exists unless replace=True
        Uses config.session.get() for accessing URLs
        """

        # Ensure the session is available
        if not hasattr(config, 'session') or not isinstance(config.session, requests.Session):
            raise RuntimeError("config.session is not properly configured")

        # Fetch the URL from self._attachments
        url = self._attachments.get(attachment)
        if not url:
            raise ValueError(f"No URL found for attachment: {attachment}")

        local_location = Path(local_location)

        # If the local location is a directory, create it if it doesn't exist
        if not local_location.suffix:
            local_location.mkdir(parents=True, exist_ok=True)
            filename = url.split('/')[-1]  # get the filename from the URL
            local_filepath = local_location / filename
        else:
            local_filepath = local_location

        # Check if file already exists
        if local_filepath.exists() and not replace:
            raise FileExistsError(f"File {local_filepath} already exists. Set replace=True to overwrite.")

        # Download the file
        response = config.session.get(url, stream=True)
        response.raise_for_status()  # Raise an error if the download failed

        # Save the file to the specified location
        with local_filepath.open('wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return local_filepath

    def upload_attachment(self, file_path):
        """Uploads an attachment to the specified URL using Selenium

        Uses config.driver for accessing the website and uploading the file
        """

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        url_suffix = f'surface/reports/surface.php?category=downlink&subsystem={self.subsystem}&sol={self.sol}'

        # Ensure the driver is available
        if not hasattr(config, 'driver') or not isinstance(config.driver, webdriver.Remote):
            config.logger.error("config.driver is not properly configured")
            raise RuntimeError("config.driver is not properly configured")

        # Ensure the file exists and convert to absolute path if necessary
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        # Ensure the file exists
        if not os.path.exists(file_path):
            config.logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        username = config.username
        password = config.password
        target_url = f'https://{username}:{password}@mslreports.jpl.nasa.gov/{url_suffix}'
        target_url_safe = f'https://mslreports.jpl.nasa.gov/{url_suffix}'

        config.driver.get(target_url)

        try:
            # Wait for the 'add attachment' link to appear and click it
            add_attachment_link = WebDriverWait(config.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="javascript:toggle_attachments"]'))
            )
            add_attachment_link.click()

            # Wait for the file input to appear, then send the file path to it
            file_input = WebDriverWait(config.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(file_path)

            # Click the 'Save' button
            save_button = WebDriverWait(config.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Save']"))
            )
            save_button.click()

            config.logger.info(f"Uploaded {file_path} to {target_url_safe}")
            return file_path, target_url_safe

        except Exception as err:
            config.logger.error(f"Failed to upload {file_path}. Error: {err}")
            raise err  # Re-raise the error to handle it further up the chain if necessary

    def _init_defaults(self):
        self.summary = None
        self.contacts = None
        self.email = None

    def _parse_email(self):
        if hasattr(self, 'contacts') and self.contacts:
            contacts = self.contacts
            contacts = contacts.lower()
            if contacts:
                for line in contacts.split('\n'):
                    if 'email:' in line or 'e-mail:' in line:
                        line = line.lstrip('email:').lstrip('e-mail:')
                    if '@' in line:
                        setattr(self, 'email', line.strip())
