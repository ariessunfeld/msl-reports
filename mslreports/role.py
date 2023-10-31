import requests
from bs4 import BeautifulSoup

from . import config
from .report import Report

class Role:
	"""Base class for MSL Reports Roles"""

	NAME = None # name as appears on MSL Reports
	DESCRIPTION = None # longer role description
	SUBSYSTEM_CODE = None # numeric code for this role's report page
	ATTACHMENTS_CODE = None # numeric code for this role's attachments page
	CATEGORY = None # uplink / downlink
	BASE_URL_REPORT = "https://mslreports.jpl.nasa.gov/surface/reports/surface.php?category={}&subsystem={}&sol={}"
	BASE_URL_TOPIC = "https://mslreports.jpl.nasa.gov/surface/reports/surface.php?category={}&subsystem={}&sol={}&topic={}"
	BASE_URL_ATTACHMENT = "https://mslreports.jpl.nasa.gov/surface/data/surface/{}/{}/"

	@classmethod
	def get_report(cls, sol):
		# Access the username and password as:
		session = config.session
		if session is None:
			raise Exception("Must connect to MSL Reports with mslreports.connect() before making requests.")
		

	@classmethod
	def _format_attachments_url(cls, sol):
		return cls.BASE_URL_ATTACHMENT.format(cls.ATTACHMENTS_CODE, sol)

	@classmethod
	def _format_report_page_url(cls, sol):
		return cls.BASE_URL_REPORT.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol)
	
	@classmethod
	def _format_report_page_topic_url(cls, sol, topic):
		return cls.BASE_URL_TOPIC.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol, topic)