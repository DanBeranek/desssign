from __future__ import annotations

import math
from typing import TYPE_CHECKING

from framesss.pre.member_1d import Member1D

from desssign.concrete.design_checks.member_1d_checks import ConcreteMember1DChecks

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt
    from framesss.enums import BeamConnection
    from framesss.enums import Element1DType
    from framesss.fea.analysis.analysis import Analysis
    from framesss.fea.node import Node

    from desssign.loads.load_case_combination import DesignLoadCaseCombination, DesignNonlinearLoadCaseCombination
    from desssign.concrete.concrete_section import ConcreteSection


class ConcreteMember1D(Member1D):
    """
    Class for 1D concrete member.

    Inherits from `Member1D` class and adds specific properties of concrete.

    :param label: A user-defined identifier for the member.
    :param element_type: Specifies the type of the element ('navier', 'timoshenko').
    :param nodes: The nodes at the ends of the member.
    :param section: The cross-section of the member.
    :param hinges: Defines the type of connections at the start and the end of the  member
                   (e.g., fixed, hinged, or semirigid) to model the rotational stiffness accurately.
    :param auxiliary_vector_xy_plane: An auxiliary vector in local xy-plane that defines the local
                                      coordinate system of the member.
    :param analysis: The :class:`Analysis` object.
    """

    section: (
        ConcreteSection  # Explicit type annotation, so that mypy can check the type
    )

    def __init__(
        self,
        label: str,
        element_type: str | Element1DType,
        nodes: list[Node],
        section: ConcreteSection,
        hinges: list[str] | list[BeamConnection],
        auxiliary_vector_xy_plane: npt.NDArray[np.float64],
        analysis: Analysis,
    ) -> None:
        """Init the WoodMember1D object."""
        super().__init__(
            label=label,
            element_type=element_type,
            nodes=nodes,
            section=section,
            hinges=hinges,
            auxiliary_vector_xy_plane=auxiliary_vector_xy_plane,
            analysis=analysis,
        )

        self.design_checks = ConcreteMember1DChecks(self)

    def perform_uls_checks(
        self, load_combinations: list[DesignLoadCaseCombination | DesignNonlinearLoadCaseCombination]
    ) -> None:
        """Perform the design checks."""
        self.design_checks.perform_uls_checks(load_combinations)
