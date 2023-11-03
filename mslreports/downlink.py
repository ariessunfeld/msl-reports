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
class LocalizationScientistReport(Report):
    def __init__(self, sol, role, topics, attachments):
        super().__init__(sol, role, topics, attachments)
        self.target_map = None
        if self.attachments:
            setattr(self, 'target_map', self.get_target_map())

    def get_target_map(self, sol=None):
        """Returns the target map covering `sol` from this report's attachments

        Parses the attachments and checks if the MSL_Targets*.jpg file for the corresponding
        sol is present; returns the link if found, None otherwise. Assumes that the
        file has a name like 'MSL_Targets_solXXXX-XXXX_*.jpg' (or jpeg or png)

        Arguments:
            sol (int): The target sol

        Returns:
            attachment name if found; None otherwise
        """
        if sol is None:
            sol = int(self.sol)
        else:
            sol = int(sol)
        for attachment in self.attachments:
            if attachment.startswith('MSL_Targets_sol') and self._is_image(attachment):
                sol_part = attachment.split('MSL_Targets_sol')[1].split('_')[0]
                if '-' in sol_part:
                    lower_bound = int(sol_part.split('-')[0])
                    upper_bound = int(sol_part.split('-')[1])
                    if sol in range(lower_bound, upper_bound + 1):
                        return attachment  # This image contains data including `sol`
                else:
                    if sol == int(sol_part):
                        return attachment  # This image contains data only for `sol`
        return None
    @staticmethod
    def _is_image(attachment):
        image_types = ['.jpg', '.jpeg', '.png']
        return any(attachment.lower().endswith(image_type) for image_type in image_types)
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


#  -----------------------------------------------


class ChemCamSPDL(Role):
    REPORT_CLASS = ChemCamSPDLReport
    NAME = "ChemCam Science PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Science Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> ChemCamSPDLReport:
        return super().get_report(*args, **kwargs)


class ChemCamEPDL(Role):
    REPORT_CLASS = ChemCamEPDLReport
    NAME = "ChemCam Eng PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Engineering Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> ChemCamEPDLReport:
        return super().get_report(*args, **kwargs)


class MastcamPDL(Role):
    REPORT_CLASS = MastcamPDLReport
    NAME = "Mastcam PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The Mastcam Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> MastcamPDLReport:
        return super().get_report(*args, **kwargs)


class MAHLIPDL(Role):
    REPORT_CLASS = MAHLIPDLReport
    NAME = "MAHLI PDL"  # name as appears on MSL Reports
    DESCRIPTION = "The MArs Hand-Lens Imager Payload Downlink Lead Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> MAHLIPDLReport:
        return super().get_report(*args, **kwargs)


class LocalizationScientist(Role):
    REPORT_CLASS = LocalizationScientistReport
    NAME = "Localization Scientist"  # name as appears on MSL Reports
    DESCRIPTION = "The Rover Localization Scientist Role"  # longer role description
    SUBSYSTEM_CODE = DOWNLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'downlink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> LocalizationScientistReport:
        return super().get_report(*args, **kwargs)
