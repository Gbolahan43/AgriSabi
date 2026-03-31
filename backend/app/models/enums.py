from enum import Enum

class Language(str, Enum):
    EN = "en"
    HA = "ha"
    YO = "yo"
    IG = "ig"
    PCM = "pcm"

class Pipeline(str, Enum):
    NOVA_SONIC = "nova_sonic"
    TRANSCRIBE = "transcribe"
    TEXT = "text"
    TWO_STAGE_DIAGNOSIS = "two_stage_diagnosis"

class SessionType(str, Enum):
    CHAT = "chat"
    VOICE = "voice"
    DIAGNOSIS = "diagnosis"
    ASSISTANT = "assistant"
