from dataclasses import dataclass
from grongier.pex import Message

from obj import Formation,Training,Patient

@dataclass
class FormationRequest(Message):
    formation:Formation = None

@dataclass
class TrainingRequest(Message):
    training:Training = None

@dataclass
class TrainingResponse(Message):
    decision:int = None

@dataclass
class PatientRequest(Message):
    patient:Patient = None
