from enum import Enum, auto


class Topics(Enum):
    SFB_T = "Safe Browsing Practices"
    PS_T = "Password Security"
    M_T = "Malware"
    SE_T = "Social Engineering"
    IR_T = "Incident Response"

class SubtopicPriority(Enum):
    HIGH = auto()
    MODERATE = auto()
    LOW = auto()
