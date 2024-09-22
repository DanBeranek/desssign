from framesss.enums import CaseInsensitiveStrEnum


class CheckResult(CaseInsensitiveStrEnum):
    """
    Enum for design results.

    :cvar PASS: Design check passed.
    :cvar FAIL: Design check failed.
    """

    PASS = "pass"
    FAIL = "fail"
