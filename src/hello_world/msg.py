from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class MyMsg(Message):
    value: str = ''