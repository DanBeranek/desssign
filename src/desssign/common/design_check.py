from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from desssign.common.enums import CheckResult

if TYPE_CHECKING:
    import numpy.typing as npt
    from framesss.pre.member_1d import Member1D
    from desssign.loads.load_case_combination import DesignLoadCaseCombination


class Check:
    """Abstract class for design checks."""

    def __init__(
        self,
        code: str,
        paragraph: str,
        equation_number: str,
    ) -> None:
        """Init the Check object."""
        self.code = code
        self.paragraph = paragraph
        self.equation_number = equation_number

    @property
    def usages(self) -> npt.NDArray[np.float64]:
        """Usages of the material at every point along the member."""
        raise NotImplementedError("Method 'usage' must be implemented.")

    @property
    def max_usage(self) -> float:
        """Maximum usage of the material."""
        return float(np.max(self.usages))

    @property
    def result(self) -> CheckResult:
        """Overall design result."""
        if self.max_usage <= 1.0:
            return CheckResult(CheckResult.PASS)
        return CheckResult(CheckResult.FAIL)


class Member1DChecks:
    """
    Abstract class for performing design checks on 1D members.
    """

    def __init__(self, member: Member1D) -> None:
        self.member = member

    @abstractmethod
    def max_usage(self) -> float:
        """Maximum usage of the material."""
        raise NotImplementedError("Method 'max_usage' must be implemented.")

    @property
    def result(self) -> CheckResult:
        """Get the overall result of the design checks."""
        if self.max_usage <= 1.0:
            return CheckResult(CheckResult.PASS)
        return CheckResult(CheckResult.FAIL)

    def get_internal_forces(
        self,
        combination: DesignLoadCaseCombination,
        include_peaks: bool = True,
    ) -> tuple[
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
    ]:
        """Get the internal forces for a given load case combination."""
        # Determine the default array sizes from the member dimensions
        default_length = self.member.x_local.shape[0]

        # Safe retrieval of internal forces using the .get method with default zero arrays
        axial = self.member.results.axial_forces.get(
            combination, np.zeros(default_length)
        )
        shear_y = self.member.results.shear_forces_y.get(
            combination, np.zeros(default_length)
        )
        shear_z = self.member.results.shear_forces_z.get(
            combination, np.zeros(default_length)
        )
        torsion = self.member.results.torsional_moments.get(
            combination, np.zeros(default_length)
        )
        bending_y = self.member.results.bending_moments_y.get(
            combination, np.zeros(default_length)
        )
        bending_z = self.member.results.bending_moments_z.get(
            combination, np.zeros(default_length)
        )

        if not include_peaks:
            return (
                axial,
                shear_y,
                shear_z,
                torsion,
                bending_y,
                bending_z,
            )

        default_peak_length = self.member.results.peak_x_local.get(
            combination, np.zeros(0)
        ).shape[0]
        axial_peaks = self.member.results.peak_axial_forces.get(
            combination, np.zeros(default_peak_length)
        )
        shear_y_peaks = self.member.results.peak_shear_forces_y.get(
            combination, np.zeros(default_peak_length)
        )
        shear_z_peaks = self.member.results.peak_shear_forces_z.get(
            combination, np.zeros(default_peak_length)
        )
        torsion_peaks = self.member.results.peak_torsional_moments.get(
            combination, np.zeros(default_peak_length)
        )
        bending_y_peaks = self.member.results.peak_bending_moments_y.get(
            combination, np.zeros(default_peak_length)
        )
        bending_z_peaks = self.member.results.peak_bending_moments_z.get(
            combination, np.zeros(default_peak_length)
        )

        # Concatenating the regular and peak forces/moments
        concatenated_axial = np.concatenate((axial, axial_peaks))
        concatenated_shear_y = np.concatenate((shear_y, shear_y_peaks))
        concatenated_shear_z = np.concatenate((shear_z, shear_z_peaks))
        concatenated_torsion = np.concatenate((torsion, torsion_peaks))
        concatenated_bending_y = np.concatenate((bending_y, bending_y_peaks))
        concatenated_bending_z = np.concatenate((bending_z, bending_z_peaks))

        return (
            concatenated_axial,
            concatenated_shear_y,
            concatenated_shear_z,
            concatenated_torsion,
            concatenated_bending_y,
            concatenated_bending_z,
        )
