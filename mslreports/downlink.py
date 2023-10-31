import requests
from bs4 import BeautifulSoup

from . import config
from .role import Role
from .report import Report

#	class Issues(Role): pass
#	class MissionLead(Role): pass
#	class TacticalDownlinkLead(Role): pass
#	class Systems(Role): pass
#	class ActivityLead(Role): pass
#	class SAPP(Role): pass
#	class DataManagement(Role): pass
#	class Mechanisms(Role): pass
#	class Mobility(Role): pass
#	class Power(Role): pass
#	class SASPAh(Role): pass
#	class Telecom(Role): pass
#	class Thermal(Role): pass
#	class Testbed(Role): pass
#	class LocalizationScientist(Role): pass
#	class PayloadDownlinkCoordinator(Role): pass
#	class APXSPDL(Role): pass
#	class ChemCamEPDL(Role): pass
#	[X]	class ChemCamSPDL(Role): pass
#	class CheMinPDL(Role): pass
#	class DANPDL(Role): pass
#	class ECAMPDL(Role): pass
#	class MastcamPDL(Role): pass
#	class MMMMDM(Role): pass
#	class MAHLIPDL(Role): pass
#	class MARDIPDL(Role): pass
#	class RADPDL(Role): pass
#	class REMSPDL(Role): pass
#	class SAMPDL(Role): pass
#	class OPGSPipelineOps(Role): pass
#	class GroundDataSystemAnalyst(Role): pass
#	class ACE(Role): pass

class ChemCamSPDLReport(Report):
	pass

class ChemCamSPDL(Role):
	NAME = None # name as appears on MSL Reports
	DESCRIPTION = None # longer role description
	SUBSYSTEM_CODE = 118 # numeric code for this role's report page
	ATTACHMENTS_CODE = None # numeric code for this role's attachments page
	CATEGORY = 'downlink' # uplink / downlink
