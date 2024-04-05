from __future__ import annotations

from typing import TYPE_CHECKING

from framesss.pre.cases import LoadCaseCombination

if TYPE_CHECKING:
    from desssign.loads.load_case import DesignLoadCase


class DesignLoadCaseCombination(LoadCaseCombination):
    """
    Represent a combination of load cases in the design process.

    :ivar label: The label of the load case combination.
    :ivar load_cases: A dictionary mapping each DesignLoadCase to its corresponding factor.
    :ivar combination_key: The key of the combination.
    """

    def __init__(
        self,
        label: str,
        load_cases: dict[DesignLoadCase, float],
        combination_key: str,
    ) -> None:
        """
        Initialize the DesignLoadCaseCombination class.

        :param label: The label of the load case combination.
        :param load_cases: A dictionary mapping each DesignLoadCase to its corresponding factor.
        :param combination_key: The key of the combination.
        """
        super().__init__(label, load_cases)  # type: ignore[arg-type]
        self.combination_key = combination_key
