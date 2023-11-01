"""Base class for MSL Reports Roles"""

import re

import requests
from bs4 import BeautifulSoup

from . import config
from .report import Report

class Role:
	"""Base class for MSL Reports Roles"""
	REPORT_CLASS = Report
	NAME = None  # name as appears on MSL Reports
	DESCRIPTION = None  # longer role description
	SUBSYSTEM_CODE = None  # numeric code for this role's report page
	CATEGORY = None  # uplink / downlink
	BASE_URL_REPORT = "https://mslreports.jpl.nasa.gov/surface/reports/surface.php?category={}&subsystem={}&sol={}"
	BASE_URL_TOPIC = "https://mslreports.jpl.nasa.gov/surface/reports/surface.php?category={}&subsystem={}&sol={}&topic={}"
	BASE_URL_ATTACHMENT = "https://mslreports.jpl.nasa.gov/surface/data/surface/{}/{}/"

	def __init__(self):
		pass

	@classmethod
	def get_report(cls, sol: int) -> REPORT_CLASS:
		"""Returns the Report for this Role on the given Sol

		Arguments:
			sol (int): The martian solar day for the report

		Returns: cls.REPORT_CLASS(sol, cls.NAME, topics_dict), where
			REPORT_CLASS is a subclass of Report,
			cls.NAME is the name the Role,
			topics_dict is a dictionary of topic content parsed from the report page
				(E.g., {'contacts': '...', 'summary': '...', 'issues':, '...'})
		"""
		config.logger.debug(f"Entered get_report with args {sol=}")

		session = config.session

		if session is None:
			err = "Must connect to MSL Reports using mslreports.connect() before making requests."
			config.logger.critical(err)
			raise Exception(err)

		# Parse topics as dictionary
		report_url = cls._format_report_page_url(sol)
		response = session.get(report_url)
		topics = cls._extract_topics_from_response(session, response, sol)

		# Parse attachments as list
		attachments_url = cls._format_attachments_url(sol)
		response = session.get(attachments_url)
		attachments = cls._extract_attachments_from_response(response, attachments_url)

		return cls.REPORT_CLASS(sol, cls, topics, attachments)

	@classmethod
	def _extract_attachments_from_response(cls, response, attachments_url):
		def link_filter(link):
			if link.startswith('?') or link.endswith('/') or link.startswith('THUMB'):
				return False
			return True

		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			links = soup.find_all('a')
			attachments_future = [link['href'] for link in links]
			return {link: f'{attachments_url}{link}' for link in filter(link_filter, attachments_future)}
		else:
			err = f"Encountered a bad status code listing attachments: {response.status_code}"
			config.logger.critical(err)
			raise Exception(err)


	@classmethod
	def _extract_topics_from_response(cls, session, response, sol):
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
				if topic_text.strip():
					topic_dict[topic] = topic_text
			return topic_dict
		else:
			err = f"Encountered a bad status code extracting topics: {response.status_code}"
			config.logger.critical(err)
			raise Exception(err)

	@classmethod
	def _format_attachments_url(cls, sol):
		return cls.BASE_URL_ATTACHMENT.format(cls.SUBSYSTEM_CODE, sol)

	@classmethod
	def _format_report_page_url(cls, sol):
		return cls.BASE_URL_REPORT.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol)

	@classmethod
	def _format_report_page_topic_url(cls, sol, topic):
		return cls.BASE_URL_TOPIC.format(cls.CATEGORY, cls.SUBSYSTEM_CODE, sol, topic)

	@classmethod
	def _find_all_topics(cls, soup: BeautifulSoup):
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
	def _extract_text_from_topic(cls, soup: BeautifulSoup):
		report_div = soup.find('div', class_='report_text')

		if not report_div:
			return None

		text_parts = []
		for child in report_div.children:
			text_part = child.get_text()
			text_part = re.sub(r'\n+', '\n', text_part)
			text_parts.append(text_part)

		ret = ' '.join(text_parts).strip().replace('\u00a0', ' ').replace('\xa0', ' ')
		ret = ret.replace('\r\n', '\n')
		ret = re.sub(r'\n+', '\n', ret)
		ret = '\n'.join([line.strip() for line in ret.split('\n') if line.strip()])
		ret = re.sub(r'\n+', '\n', ret)
		return ret
