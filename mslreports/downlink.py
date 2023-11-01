"""Concrete Report and Role classes for all Downlink roles

TODO: Define concrete Role subclasses for all Downlink roles
TODO: Add parsing logic to Report subclasses as necessary (see .uplink.ChemCamSPULReport for example)
"""

import requests
from bs4 import BeautifulSoup

from . import config
from .role import Role
from .report import Report
from .constants import DOWNLINK_CODES

class IssuesReport(Report): pass
class MissionLeadReport(Report): pass
class TacticalDownlinkLeadReport(Report): pass
class SystemsReport(Report): pass
class ActivityLeadReport(Report): pass
class SAPPReport(Report): pass
class DataManagementReport(Report): pass
class MechanismsReport(Report): pass
class MobilityReport(Report): pass
class PowerReport(Report): pass
class SASPAhReport(Report): pass
class TelecomReport(Report): pass
class ThermalReport(Report): pass
class TestbedReport(Report): pass
class LocalizationScientistReport(Report): pass
class PayloadDownlinkCoordinatorReport(Report): pass
class APXSPDLReport(Report): pass
class ChemCamEPDLReport(Report): pass
class ChemCamSPDLReport(Report): pass
class CheMinPDLReport(Report): pass
class DANPDLReport(Report): pass
class ECAMPDLReport(Report): pass
class MastcamPDLReport(Report): pass
class MMMMDMReport(Report): pass
class MAHLIPDLReport(Report): pass
class MARDIPDLReport(Report): pass
class RADPDLReport(Report): pass
class REMSPDLReport(Report): pass
class SAMPDLReport(Report): pass
class OPGSPipelineOpsReport(Report): pass
class GroundDataSystemAnalystReport(Report): pass
class ACEReport(Report): pass


class ChemCamSPDL(Role):
    REPORT_CLASS = ChemCamSPDLReport
    NAME = "ChemCam Science PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Science Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, sol: int) -> ChemCamSPDLReport:
        return super().get_report(sol)


class ChemCamEPDL(Role):
    REPORT_CLASS = ChemCamEPDLReport
    NAME = "ChemCam Eng PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Engineering Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, sol: int) -> ChemCamEPDLReport:
        return super().get_report(sol)


class MastcamPDL(Role):
    REPORT_CLASS = MastcamPDLReport
    NAME = "Mastcam PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The Mastcam Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, sol: int) -> MastcamPDLReport:
        return super().get_report(sol)


class MAHLIPDL(Role):
    REPORT_CLASS = MAHLIPDLReport
    NAME = "MAHLI PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The MArs Hand-Lens Imager Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, sol: int) -> MAHLIPDLReport:
        return super().get_report(sol)
