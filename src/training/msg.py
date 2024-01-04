from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class FormationRequest(Message):
    id: int = 0
    nom: str = ''
    salle: str = ''