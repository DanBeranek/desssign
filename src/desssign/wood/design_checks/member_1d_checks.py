from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from desssign.common.design_check import Member1DChecks
from desssign.wood.design_checks.design_check import BeamStabilityCheck
from desssign.wood.design_checks.design_check import ColumnStabilityCheck
from desssign.wood.design_checks.design_check import (
    CombinedBendingAndAxialCompressionCheck,
)
from desssign.wood.design_checks.design_check import CombinedBendingAndAxialTensionCheck
from desssign.wood.design_checks.design_check import ShearCheck

if TYPE_CHECKING:
    from desssign.loads.load_case_combination import DesignLoadCaseCombination
    from desssign.wood.wood_member import WoodMember1D


class WoodMember1DChecks(Member1DChecks):
    """
    Class for performing design checks on 1D members.

    :param member: The 1D wood member.
    """

    member: WoodMember1D  # Explicit type annotation, so that mypy can check the type

    def __init__(self, member: WoodMember1D) -> None:
        """Init the WoodMember1DChecks object."""
        super().__init__(member=member)

        self.column_stability: dict[DesignLoadCaseCombination, ColumnStabilityCheck] = (
            {}
        )
        self.beam_stability: dict[DesignLoadCaseCombination, BeamStabilityCheck] = {}

        self.shear_check: dict[DesignLoadCaseCombination, ShearCheck] = {}
        self.tension_with_bending_check: dict[
            DesignLoadCaseCombination, CombinedBendingAndAxialTensionCheck
        ] = {}
        self.compression_with_bending_check: dict[
            DesignLoadCaseCombination, CombinedBendingAndAxialCompressionCheck
        ] = {}

    @property
    def max_usage(self) -> float:
        """Get the maximum usage of the design checks."""
        max_usages = [
            check.max_usage
            for check in (
                *self.column_stability.values(),
                *self.beam_stability.values(),
                *self.shear_check.values(),
                *self.tension_with_bending_check.values(),
                *self.compression_with_bending_check.values(),
            )
        ]
        return max(max_usages)

    def perform_uls_checks(
        self, load_case_combinations: list[DesignLoadCaseCombination]
    ) -> None:
        """
        Perform all design checks on the member for given load case combinations.

        :param load_case_combinations: The list of load case combinations to check.
        """
        self.perform_column_stability_checks(load_case_combinations)
        self.perform_beam_stability_checks(load_case_combinations)
        self.perform_shear_checks(load_case_combinations)
        self.perform_tension_with_bending_checks(load_case_combinations)
        self.perform_compression_with_bending_checks(load_case_combinations)

    def perform_column_stability_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        """Perform the column stability checks for the given load case combinations."""
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, bending_z = self.get_internal_forces(combination)

            sigma_c0d = axial / self.member.section.area_x
            sigma_c0d[sigma_c0d >= 0] = 0

            sigma_myd = bending_y / self.member.section.W_y
            sigma_mzd = bending_z / self.member.section.W_z

            f_c0d = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_c0k,
                load_duration_class=combination.load_duration_class,
            )

            f_md = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_mk,
                load_duration_class=combination.load_duration_class,
            )

            self.column_stability[combination] = ColumnStabilityCheck(
                sigma_c0d=sigma_c0d,
                sigma_myd=sigma_myd,
                sigma_mzd=sigma_mzd,
                f_c0d=f_c0d,
                f_myd=f_md,
                f_mzd=f_md,
                k_cy=self.member.k_cy,
                k_cz=self.member.k_cz,
                k_m=self.member.section.k_m,
            )

    def perform_beam_stability_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        """Perform the beam stability checks for the given load case combinations."""
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, bending_z = self.get_internal_forces(combination)

            sigma_c0d = axial / self.member.section.area_x
            sigma_c0d[sigma_c0d >= 0] = 0

            sigma_myd = bending_y / self.member.section.W_y

            f_c0d = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_c0k,
                load_duration_class=combination.load_duration_class,
            )

            f_md = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_mk,
                load_duration_class=combination.load_duration_class,
            )

            self.beam_stability[combination] = BeamStabilityCheck(
                sigma_c0d=sigma_c0d,
                sigma_myd=sigma_myd,
                f_c0d=f_c0d,
                f_myd=f_md,
                k_crit=self.member.k_crit,
                k_cz=self.member.k_cz,
            )

    def perform_shear_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        """Perform the shear checks for the given load case combinations."""
        for combination in load_case_combinations:
            _, shear_y, shear_z, _, _, _ = self.get_internal_forces(combination)

            k_cr = self.member.section.k_cr
            tau_d = 3 * np.abs(shear_z) / (2 * k_cr * self.member.section.area_z)

            f_vd = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_vk,
                load_duration_class=combination.load_duration_class,
            )

            self.shear_check[combination] = ShearCheck(
                tau_d=tau_d,
                f_vd=f_vd,
            )

    def perform_tension_with_bending_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        """Perform the tension with bending checks for the given load case combinations."""
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, bending_z = self.get_internal_forces(combination)

            sigma_t0d = axial / self.member.section.area_x
            sigma_t0d[sigma_t0d < 0] = 0

            sigma_myd = bending_y / self.member.section.W_y
            sigma_mzd = bending_z / self.member.section.W_z

            f_cd = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_c0k,
                load_duration_class=combination.load_duration_class,
            )
            f_md = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_mk,
                load_duration_class=combination.load_duration_class,
            )

            self.tension_with_bending_check[combination] = (
                CombinedBendingAndAxialTensionCheck(
                    sigma_t0d=sigma_t0d,
                    sigma_myd=sigma_myd,
                    sigma_mzd=sigma_mzd,
                    f_t0d=f_cd,
                    f_myd=f_md,
                    f_mzd=f_md,
                    k_m=self.member.section.k_m,
                )
            )

    def perform_compression_with_bending_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination],
    ) -> None:
        """Perform the compression with bending checks for the given load case combinations."""
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, bending_z = self.get_internal_forces(combination)

            sigma_c0d = axial / self.member.section.area_x
            sigma_c0d[sigma_c0d >= 0] = 0

            sigma_myd = bending_y / self.member.section.W_y
            sigma_mzd = bending_z / self.member.section.W_z

            f_c0d = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_c0k,
                load_duration_class=combination.load_duration_class,
            )
            f_md = self.member.section.material.get_design_value(
                characteristic_value=self.member.section.material.f_mk,
                load_duration_class=combination.load_duration_class,
            )

            self.compression_with_bending_check[combination] = (
                CombinedBendingAndAxialCompressionCheck(
                    sigma_c0d=sigma_c0d,
                    sigma_myd=sigma_myd,
                    sigma_mzd=sigma_mzd,
                    f_c0d=f_c0d,
                    f_myd=f_md,
                    f_mzd=f_md,
                    k_m=self.member.section.k_m,
                )
            )
