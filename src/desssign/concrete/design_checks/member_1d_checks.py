from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from desssign.common.design_check import Member1DChecks
from desssign.concrete.design_checks.design_check import BendingCheck

if TYPE_CHECKING:
    import numpy.typing as npt

    from desssign.loads.load_case_combination import DesignLoadCaseCombination
    from desssign.concrete.concrete_member import ConcreteMember1D


class ConcreteMember1DChecks(Member1DChecks):
    """
    Class for performing design checks on 1D members.

    :param member: The 1D concrete member.
    """

    member: ConcreteMember1D  # Explicit type annotation, so that mypy can check the type

    def __init__(
        self,
        member: ConcreteMember1D
    ):
        super().__init__(member=member)

        self.bending_check: dict[DesignLoadCaseCombination, BendingCheck] = {}

    @property
    def max_usage(self) -> float:
        """Maximum usage of the material."""
        max_usages = [
            check.max_usage
            for check in (
                *self.bending_check.values(),
            )
        ]
        return max(max_usages)

    def perform_uls_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        self.perform_bending_checks(load_case_combinations)

    def perform_bending_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, _ = self.get_internal_forces(combination)

            self.bending_check[combination] = BendingCheck(
                m_ed=bending_y,
                m_rd_positive=self.member.section.m_rd_positive,
                m_rd_negative=self.member.section.m_rd_negative
            )
