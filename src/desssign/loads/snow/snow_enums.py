from framesss.enums import CaseInsensitiveStrEnum


class Topography(CaseInsensitiveStrEnum):
    """Enumeration of topographies."""

    WINDSWEPT = "windswept"
    NORMAL = "normal"
    SHELTERED = "sheltered"


class SnowZone(CaseInsensitiveStrEnum):
    """Enumeration of snow zones."""

    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"
    VI = "VI"
    VII = "VII"
    VIII = "VIII"
