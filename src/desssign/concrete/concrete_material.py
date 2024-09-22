from __future__ import annotations

import math as math

from framesss.pre.material import Material

from desssign.concrete.strength_classes import CONCRETE_STRENGTH_CLASSES
from desssign.concrete.constants import PARTIAL_FACTOR_CONCRETE, ALPHA_CC, ALPHA_CT


class ConcreteMaterial(Material):
    """
    Class for structural concrete material.

    Inherits from Material class and adds specific properties of concrete.

    :param strength_class: Strength class of the concrete material.
    """

    def __init__(
        self,
        strength_class: str | None = None,
        f_ck: float | None = None,
        gamma_c: float = PARTIAL_FACTOR_CONCRETE,
        alpha_cc: float = ALPHA_CC,
        alpha_ct: float = ALPHA_CT,
    ) -> None:
        """Initialise concrete material properties."""
        self.strength_class = strength_class

        if strength_class is not None:
            if strength_class not in CONCRETE_STRENGTH_CLASSES.keys():
                raise ValueError(
                    f"Concrete strength class '{strength_class}' not recognised. "
                    f"Choose from: {[c for c in CONCRETE_STRENGTH_CLASSES.keys()]}."
                )
            self.f_ck = CONCRETE_STRENGTH_CLASSES.get(strength_class)
        else:
            if f_ck is None:
                raise ValueError(
                    "Concrete strength class or characteristic "
                    "compressive cylinder strength must be provided."
                )
            if f_ck <= 0:
                raise ValueError(
                    "Characteristic compressive cylinder strength of concrete must be positive."
                )
            self.f_ck = f_ck

        self.gamma_c = gamma_c
        self.alpha_cc = alpha_cc
        self.alpha_ct = alpha_ct

        poisson = 0.2  # TODO: Add Poisson's ratio

        super().__init__(
            label=strength_class,
            elastic_modulus=self.e_cm,
            poissons_ratio=poisson,
            thermal_expansion_coefficient=10e-6,  # According to EN 1995-1-5, table C.1
            density=2400,
        )

    def __repr__(self) -> str:
        """Return the string representation of the WoodMaterial object."""
        return f"ConcreteMaterial({self.strength_class})"

    @property
    def f_cd(self) -> float:
        """
        Design compressive strength of concrete [Pa].

        EN 1992-1-1:2004, Eq. (3.15).
        """
        return self.alpha_cc * self.f_ck / self.gamma_c

    @property
    def f_ctd(self) -> float:
        """
        Design tensile strength of concrete [Pa].

        EN 1992-1-1:2004, Eq. (3.16).
        """
        return self.alpha_ct * self.f_ctk_0_05 / self.gamma_c

    @property
    def f_cm(self) -> float:
        """Mean value of concrete cylinder compressive strength [Pa]."""
        return self.f_ck + 8e6

    @property
    def f_ctm(self) -> float:
        """Mean value of axial tensile strength of concrete [Pa]."""
        if self.f_ck <= 50e6:
            f_ctm = 0.3 * self.f_ck ** (2 / 3)
        else:
            f_ctm = 2.12 * math.log(1 + (self.f_cm / 1e6) / 10)
        return f_ctm

    @property
    def f_ctk_0_05(self) -> float:
        """5% fractile of characteristic axial tensile strength of concrete [Pa]."""
        return 0.7 * self.f_ctm

    @property
    def f_ctk_0_95(self) -> float:
        """95% fractile of characteristic axial tensile strength of concrete [Pa]."""
        return 1.3 * self.f_ctm

    @property
    def e_cm(self) -> float:
        """Mean value of concrete compressive modulus of elasticity [Pa]."""
        return (22 * ((self.f_cm / 1e6) / 10) ** 0.3) * 1e9

    @property
    def eps_c1(self) -> float:
        """Compressive strain in the concrete at the peak stress f_cm [1]."""
        return min(0.7 * (self.f_cm / 1e6) ** 0.31, 2.8) / 1000

    @property
    def eps_cu1(self) -> float:
        """Ultimate compressive strain in the concrete [1]."""
        if self.f_ck <= 50e6:
            return 0.0035
        else:
            return (2.8 + 27 * ((98 - (self.f_cm / 1e6)) / 100) ** 4) / 1000

    @property
    def eps_c2(self) -> float:
        """Compressive strain in the concrete separating the parabolic and constant part [1]."""
        if self.f_ck <= 50e6:
            return 0.002
        else:
            return (2 + 0.085 * ((self.f_ck / 1e6) - 50) ** 0.53) / 1000

    @property
    def eps_cu2(self) -> float:
        """Ultimate compressive strain in the concrete [1]."""
        if self.f_ck <= 50e6:
            return 0.0035
        else:
            return (2.6 + 35 * ((90 - (self.f_ck / 1e6)) / 100) ** 4) / 1000

    @property
    def n(self) -> float:
        """Exponent for calculating the parabolic stress-strain curve of concrete [1]."""
        if self.f_ck <= 50e6:
            return 2.0
        else:
            return 1.4 + 23.4 * ((90 - (self.f_ck / 1e6)) / 100) ** 4

    @property
    def eps_c3(self) -> float:
        """Compressive strain in the concrete separating the linear and constant part [1]."""
        if self.f_ck <= 50e6:
            return 0.002
        else:
            return (1.75 + 0.55 * (((self.f_ck / 1e6) - 50) / 40)) / 1000

    @property
    def eps_cu3(self) -> float:
        """Ultimate compressive strain in the concrete [1]."""
        if self.f_ck <= 50e6:
            return 0.0035
        else:
            return (2.6 + 35 * ((90 - (self.f_ck / 1e6)) / 100) ** 4) / 1000

    @property
    def eta(self) -> float:
        """Parameter defining effective strength of a rectangular stress distribution [1]."""
        if self.f_ck <= 50e6:
            return 1.0
        else:
            return 1.0 - ((self.f_ck / 1e6) - 50.0) / 200.0

    @property
    def lamb(self) -> float:
        """Effective height coefficient of the compression area in rectangular stress distribution [1]."""
        if self.f_ck <= 50e6:
            return 0.8
        else:
            return 0.8 - ((self.f_ck / 1e6) - 50.0) / 200.0
