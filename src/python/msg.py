from dataclasses import dataclass
from xmlrpc.client import Boolean
from grongier.pex import Message

from obj import Formation,Training,Patient

@dataclass
class FormationRequest(Message):
    formation:Formation = None

@dataclass
class TrainingIrisRequest(Message):
    training:Training = None

@dataclass
class TrainingIrisResponse(Message):
    bool:Boolean = None

@dataclass
class PatientRequest(Message):
    patient:Patient = None
