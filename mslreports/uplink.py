import re

import requests
from bs4 import BeautifulSoup

from . import config
from .role import Role
from .report import Report


#	class IssuesForNextPlan: pass
#	class SolScenario: pass
#	class SeqDeviations: pass
#	class IPESupraTactical: pass
#	class MissionLead: pass
#	class TacticalUplinkLead: pass
#	class EngineeringUplinkLead: pass
#	class SciencePlanner: pass
#	class SequenceIntegrationEngineer: pass
#	class DataManagement: pass
#	class RoverPlanner: pass
#	class SOWGChairSUR: pass
#	class SOWGDocumentarian: pass
#	class LongTermPlanner: pass
#	class SSSScientist: pass
#	class SurfacePropertiesScientist: pass
#	class APXSPUL: pass
#	class ChemCamEPUL: pass
#	[X]	class ChemCamSPUL: pass
#	class CheMinPUL: pass
#	class DANPUL: pass
#	class ECAMPUL: pass
#	class MastcamPUL: pass
#	class MAHLIPUL: pass
#	class MARDIPUL: pass
#	class MMMMTL: pass
#	class RADIUSPUL: pass
#	class REMSPUL: pass
#	class SAMPUL: pass

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


class ChemCamSPUL(Role):
    REPORT_CLASS = ChemCamSPULReport
    NAME = "ChemCam Science PUL"  # name as appears on MSL Reports
    DESCRIPTION = "The ChemCam Science Payload Uplink Lead Role"  # longer role description
    SUBSYSTEM_CODE = 116  # numeric code for this role's report page
    CATEGORY = 'uplink'  # uplink / downlink

    @classmethod
    def get_report(cls, sol: int) -> ChemCamSPULReport:
        return super().get_report(sol)
