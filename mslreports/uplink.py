import requests
from bs4 import BeautifulSoup

from . import config
from .role import Role

# class IssuesForNextPlan: pass
# class SolScenario: pass
# class SeqDeviations: pass
# class IPESupraTactical: pass
# class MissionLead: pass
# class TacticalUplinkLead: pass
# class EngineeringUplinkLead: pass
# class SciencePlanner: pass
# class SequenceIntegrationEngineer: pass
# class DataManagement: pass
# class RoverPlanner: pass
# class SOWGChairSUR: pass
# class SOWGDocumentarian: pass
# class LongTermPlanner: pass
# class SSSScientist: pass
# class SurfacePropertiesScientist: pass
# class APXSPUL: pass
# class ChemCamEPUL: pass
# class ChemCamSPUL: pass
# class CheMinPUL: pass
# class DANPUL: pass
# class ECAMPUL: pass
# class MastcamPUL: pass
# class MAHLIPUL: pass
# class MARDIPUL: pass
# class MMMMTL: pass
# class RADIUSPUL: pass
# class REMSPUL: pass
# class SAMPUL: pass

class ChemCamPUL(Role)