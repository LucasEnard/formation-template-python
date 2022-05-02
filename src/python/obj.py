from dataclasses import dataclass

@dataclass
class Formation:
    id_formation:int = None
    nom:str = None
    salle:str = None

@dataclass
class Training:
    name:str = None
    room:str = None

@dataclass
class Patient:
    name:str = None
    infos = None
    avg:int = None
