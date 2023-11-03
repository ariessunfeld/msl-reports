"""Concrete Report and Role classes for all Uplink roles

TODO: Define concrete Role subclasses for all Uplink roles
TODO: Add parsing logic to Report subclasses as necessary (see ChemCamSPULReport example)
"""

import re

import requests
from bs4 import BeautifulSoup

from . import config
from .role import Role
from .report import Report
from .constants import UPLINK_CODES

class IssuesForNextPlanReport(Report): pass
class SolScenarioReport(Report): pass
class SeqDeviationsReport(Report): pass
class IPESupraTacticalReport(Report): pass
class MissionLeadReport(Report): pass
class TacticalUplinkLeadReport(Report): pass
class EngineeringUplinkLeadReport(Report): pass
class SciencePlannerReport(Report): pass
class SequenceIntegrationEngineerReport(Report): pass
class DataManagementReport(Report): pass
class RoverPlannerReport(Report): pass
class SOWGChairSURReport(Report): pass
class SOWGDocumentarianReport(Report): pass
class LongTermPlannerReport(Report): pass
class SSSScientistReport(Report): pass
class SurfacePropertiesScientistReport(Report): pass
class APXSPULReport(Report): pass
class ChemCamEPULReport(Report): pass
class CheMinPULReport(Report): pass
class DANPULReport(Report): pass
class ECAMPULReport(Report): pass
class MastcamPULReport(Report): pass
class MAHLIPULReport(Report): pass
class MARDIPULReport(Report): pass
class MMMMTLReport(Report): pass
class RADIUSPULReport(Report): pass
class REMSPULReport(Report): pass
class SAMPULReport(Report): pass

class ChemCamSPULReport(Report):
    def __init__(self, sol, role, topics, attachments):
        super().__init__(sol, role, topics, attachments)
        self.details = None
        if 'summary' in self.topics:
            setattr(self, 'details', self._parse_details_from_summary())

    def _parse_details_from_summary(self):
        summary = self.summary
        details_section_future = summary.split('Details', 1)
        if len(details_section_future) > 1:
            details_section_future = details_section_future[1]
            details_section = details_section_future.split('N+1')[0]
            # sequences = details_section.split("SeqId:")
            sequences = self.split_on_seq_id(details_section)
            all_sequences = []
            if len(sequences) > 1:
                for sequence in sequences[1:]:  # skip the first split as it's before the first SeqId
                    sequence = 'SeqID: ' + sequence.lstrip().lstrip(':')
                    lines = sequence.strip().split("\n")
                    seq_dict = {}
                    for line in lines:
                        if ':' in line:
                            key, value = line.split(":", 1)  # split by the first occurrence of ': '
                            seq_dict[key.strip()] = value.strip()
                    all_sequences.append(seq_dict)
            return all_sequences

    @staticmethod
    def split_on_seq_id(text):
        # Using the case-insensitive flag (?i)
        return re.split(r'(?i)SeqID:', text)


#  -------------------------------------------------


class ChemCamSPUL(Role):
    REPORT_CLASS = ChemCamSPULReport
    NAME = "ChemCam Science PUL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Science Payload Uplink Lead Role"  # longer role description
    SUBSYSTEM_CODE = UPLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'uplink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> ChemCamSPULReport:
        return super().get_report(*args, **kwargs)


class ChemCamEPUL(Role):
    REPORT_CLASS = ChemCamEPULReport
    NAME = "ChemCam Eng PUL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Engineering Payload Uplink Lead Role"  # longer role description
    SUBSYSTEM_CODE = UPLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'uplink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> ChemCamEPULReport:
        return super().get_report(*args, **kwargs)


class MastcamPUL(Role):
    REPORT_CLASS = MastcamPULReport
    NAME = "Mastcam PUL"  # name as appears on MSL Reports
    DESCRIPTION = "The Mastcam Payload Uplink Lead Role"  # longer role description
    SUBSYSTEM_CODE = UPLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'uplink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> MastcamPULReport:
        return super().get_report(*args, **kwargs)


class APXSPUL(Role):
    REPORT_CLASS = APXSPULReport
    NAME = "APXS PUL"  # name as appears on MSL Reports
    DESCRIPTION = "The Alpha Particle Xray Spectrometer (APXS) Payload Uplink Lead Role"  # longer role description
    SUBSYSTEM_CODE = UPLINK_CODES[NAME]  # numeric code for this role's report page
    CATEGORY = 'uplink'  # uplink / downlink

    @classmethod
    def get_report(cls, *args, **kwargs) -> APXSPULReport:
        return super().get_report(*args, **kwargs)
