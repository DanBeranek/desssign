from __future__ import annotations

from typing import TYPE_CHECKING

from framesss.pre.section import PolygonalSection

if TYPE_CHECKING:
    from desssign.concrete.concrete_material import ConcreteMaterial
    from desssign.concrete.rebar_material import RebarMaterial


class ConcreteSection(PolygonalSection):
    """
    Class for concrete section.

    Inherits from `Section` class and adds specific properties of concrete section.

    :param label: Label of the section.
    :param points: Points defining boundary of the section.
    :param material: Material of the section.
    :param b_w: Smallest width of the cross-section in the tensile area.
    :param A_sl: Area of the tensile reinforcement.
    :param m_rd_positive: Bending moment resistance.
    :param m_rd_negative: Bending moment resistance.
    """

    material: ConcreteMaterial  # Explicit type annotation, so that mypy can check the type

    def __init__(
        self,
        label: str,
        points: list[list[float]],
        material: ConcreteMaterial,
        b_w: float,
        A_sl: float,
        m_rd_positive: float,
        m_rd_negative: float,
    ) -> None:
        super().__init__(
            label=label,
            points=points,
            material=material
        )

        self.b_w = b_w
        self.A_sl = A_sl
        self.m_rd_positive = m_rd_positive
        self.m_rd_negative = m_rd_negative
