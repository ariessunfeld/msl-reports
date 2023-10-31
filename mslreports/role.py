import re

import requests
from bs4 import BeautifulSoup

from . import config
from .report import Report

class Role:
	"""Base class for MSL Reports Roles"""

	REPORT_CLASS = Report
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
		report_url = cls._format_report_page_url(sol)
		response = session.get(report_url)
		if response.status_code == 200:
			topic_dict = {}
			soup = BeautifulSoup(response.content, 'html.parser')
			topics = cls._find_all_topics(soup)
			if topics is None:
				return None
			for topic in topics:
				report_topic_url = cls._format_report_page_topic_url(sol, topic)
				topic_response = session.get(report_topic_url)
				topic_soup = BeautifulSoup(topic_response.content, 'html.parser')
				topic_text = cls._extract_text_from_topic(topic_soup)
				topic_text = re.sub(r'\n+', '\n', topic_text)
				if topic_text.strip():
					topic_dict[topic] = topic_text
			return cls.REPORT_CLASS(sol, cls.NAME, topic_dict)
		else:
			raise Exception(f"Encountered a bad status code: {response.status_code}")


	@classmethod
	def _format_attachments_url(cls, sol):
		return cls.BASE_URL_ATTACHMENT.format(cls.ATTACHMENTS_CODE, sol)

	@classmethod
	def _format_report_page_url(cls, sol):
		return cls.BASE_URL_REPORT.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol)
	
	@classmethod
	def _format_report_page_topic_url(cls, sol, topic):
		return cls.BASE_URL_TOPIC.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol, topic)

	@classmethod
	def _find_all_topics(cls, soup : BeautifulSoup):
		"""Returns list of topics parsed from div"""
		target_div = soup.find('div', style="margin:30px 5px 0 5px;")
		if target_div:
			topics = []
			for a_tag in target_div.find_all('a', recursive=False):
				href = a_tag.get('href', '')
				if '&topic=' in href:
					topic = href.split('&topic=')[-1]
					if topic not in topics:
						topics.append(topic)
			return topics
		else:
			return None

	@classmethod
	def _extract_text_from_topic(cls, soup : BeautifulSoup):
		
		report_div = soup.find('div', class_='report_text')
		
		if not report_div:
			return None

		text_parts = []
		for child in report_div.children:
			text_parts.append(child.get_text())

		return ' '.join(text_parts).strip().replace('\u00a0', ' ').replace('\xa0', ' ')