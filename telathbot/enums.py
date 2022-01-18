from enum import Enum


class SafetyToolsLevels(str, Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    ALL = "all"
