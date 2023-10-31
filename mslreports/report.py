"""Base class for MSLReports `Report` objects"""

import json

from .constants import TOPIC_URL_TO_FUNC_NAME

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
    def __init__(self, sol, role, topics):
        self.sol = sol
        self.role = role
        self._topics = topics
        self.topics = []
        self._init_defaults()

        for topic_key, topic_content in self._topics.items():
            pythonic_name = TOPIC_URL_TO_FUNC_NAME.get(topic_key, None)
            if pythonic_name:
                setattr(self, pythonic_name, topic_content)
                self.topics.append(pythonic_name)

        self._parse_email()

    def _init_defaults(self):
        self.summary = None
        self.contacts = None
        self.email = None

    def _parse_email(self):
        if hasattr(self, 'contacts'):
            contacts = self.contacts
            contacts = contacts.lower()
            if contacts:
                for line in contacts.split('\n'):
                    if 'email:' in line or 'e-mail:' in line:
                        line = line.lstrip('email:').lstrip('e-mail:')
                    if '@' in line:
                        setattr(self, 'email', line.strip())
