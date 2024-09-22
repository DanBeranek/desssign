from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import math

from desssign.common.design_check import Check

if TYPE_CHECKING:
    import numpy.typing as npt


class BendingCheck(Check):
    """
    Class for checking bending.

    :param m_ed: Bending moments along the member.
    :param m_rd_positive: Ultimate resistance of reinforced section.
    :param m_rd_negative: Ultimate resistance of reinforced section.
    """

    def __init__(
        self,
        m_ed: npt.NDArray[np.float64],
        m_rd_positive: float,
        m_rd_negative: float,
    ) -> None:
        """Init the BendingCheck object."""
        super().__init__("EN 1992-1-1", "", "6.1")
        self.m_ed = m_ed
        self.m_rd_positive = m_rd_positive
        self.m_rd_negative = m_rd_negative

    @property
    def usages(self) -> npt.NDArray[np.float64]:
        """Usages of the material at every point along the member."""
        usages = np.zeros(self.m_ed.shape)
        usages[self.m_ed >= 0] = self.m_ed[self.m_ed >= 0] / self.m_rd_positive
        usages[self.m_ed < 0] = self.m_ed[self.m_ed < 0] / self.m_rd_negative
        return usages


class ShearCheckWithoutShearReinforcement(Check):
    def __init__(
        self,
        v_ed: npt.NDArray[np.float64],
        f_ck: float,
        d: float,
        b_w: float,
        A_sl: float,
        c_rd_c: float = 0.18 / 1.15,
    ) -> None:
        """
        Init the ShearCheck object.

        :param f_ck: Characteristic concrete cylinder strength in MPa.
        :param d: Rebar diameter in mm.
        :param b_w: Smallest width of the cross-section in the tensile area.
        :param A_sl: Area of the tensile reinforcement.
        """
        super().__init__("EN 1992-1-1", "6.2", "6.2.a, 6.2.b")
        k = min(1 + math.sqrt(200 / d), 2.0)
        rho_l = min(A_sl / (b_w * d), 0.02)

        v_min = 0.035 * k ** (3 / 2) * f_ck ** (1 / 2)

        v_rd_c_a = (c_rd_c * k * (100 * rho_l * f_ck) ** (1 / 3)) * b_w * d
        v_rd_c_b = v_min * b_w * d

        self.v_rd_c = min(v_rd_c_a, v_rd_c_b)
        self.v_ed = v_ed

    @property
    def usages(self) -> npt.NDArray[np.float64]:
        """Usages of the material at every point along the member."""
        return np.abs(self.v_ed) / self.v_rd_c
