from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from framesss.pre.cases import EnvelopeCombination

from desssign.common.design_check import Member1DChecks
from desssign.concrete.design_checks.design_check import BendingCheck
from desssign.concrete.design_checks.design_check import ShearCheck

if TYPE_CHECKING:
    import numpy.typing as npt

    from desssign.loads.load_case_combination import DesignLoadCaseCombination
    from desssign.concrete.concrete_member import ConcreteMember1D


class ConcreteMember1DChecks(Member1DChecks):
    """
    Class for performing design checks on 1D members.

    :param member: The 1D concrete member.
    """

    member: (
        ConcreteMember1D  # Explicit type annotation, so that mypy can check the type
    )

    def __init__(self, member: ConcreteMember1D):
        super().__init__(member=member)

        self.bending_check: (dict[DesignLoadCaseCombination, BendingCheck] |
                             dict[EnvelopeCombination, list[BendingCheck, BendingCheck]]) = {}
        self.shear_check: (dict[DesignLoadCaseCombination, ShearCheck] |
                           dict[EnvelopeCombination, ShearCheck]) = {}

    @property
    def max_usage(self) -> float:
        """Maximum usage of the material."""
        max_usages = [check.max_usage for check in (*self.bending_check.values(),)]
        return max(max_usages)

    def perform_uls_checks(
        self,
        load_case_combinations: list[DesignLoadCaseCombination] | EnvelopeCombination
    ) -> None:
        if isinstance(load_case_combinations, EnvelopeCombination):
            self.perform_envelope_uls_checks(load_case_combinations)
        elif isinstance(load_case_combinations, list):
            self.perform_combinations_uls_checks(load_case_combinations)
        else:
            raise ValueError(f"Wrong 'load_case_combination' type: {type(load_case_combinations)}")

    def perform_envelope_uls_checks(self, envelope: EnvelopeCombination) -> None:
        self.perform_bending_checks_envelope(envelope)
        self.perform_shear_checks_envelope(envelope)

    def perform_combinations_uls_checks(self, combinations: list[DesignLoadCaseCombination]) -> None:
        self.perform_bending_checks_combinations(combinations)
        self.perform_shear_checks_combinations(combinations)

    def get_moments_of_resistance(self) -> tuple[float, float] | tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        if self.member.section:
            m_rd_positive = self.member.section.m_rd_positive
            m_rd_negative = self.member.section.m_rd_negative
        else:
            m_rd_positive = []
            m_rd_negative = []
            for elem in self.member.generated_elements:
                m_rd_positive.extend(np.full(
                    shape=elem.sampling_points.shape,
                    fill_value=elem.section.m_rd_positive,
                ).tolist()
                                     )
                m_rd_negative.extend(np.full(
                    shape=elem.sampling_points.shape,
                    fill_value=elem.section.m_rd_negative,
                ).tolist()
                                     )
            m_rd_positive = np.array(m_rd_positive)
            m_rd_negative = np.array(m_rd_negative)

        return m_rd_positive, m_rd_negative

    def get_shear_force_resistance(self) -> float | npt.NDArray[np.float64]:
        if self.member.section:
            return self.member.section.v_rd
        else:
            v_rd = []
            for elem in self.member.generated_elements:
                v_rd.extend(
                    np.full(
                        shape=elem.sampling_points.shape,
                        fill_value=elem.section.v_rd
                    ).tolist()
                )

            return np.array(v_rd)

    def perform_bending_checks_combinations(self, load_case_combinations: list[DesignLoadCaseCombination]) -> None:
        for combination in load_case_combinations:
            axial, _, _, _, bending_y, _ = self.get_internal_forces(combination, include_peaks=False)

            m_rd_positive, m_rd_negative = self.get_moments_of_resistance()

            self.bending_check[combination] = BendingCheck(
                m_ed=bending_y,
                m_rd_positive=m_rd_positive,
                m_rd_negative=m_rd_negative,
            )

    def perform_shear_checks_combinations(self, load_case_combinations: list[DesignLoadCaseCombination]) -> None:
        for combination in load_case_combinations:
            _, _, shear_z, _, _, _ = self.get_internal_forces(combination, include_peaks=False)

            v_rd = self.get_shear_force_resistance()

            self.shear_check[combination] = ShearCheck(
                v_ed=shear_z,
                v_rd=v_rd
            )

    def perform_shear_checks_envelope(self, envelope: EnvelopeCombination) -> None:
        pos_neg_shear_z = self.member.results.shear_forces_z.get(envelope)

        shear_z = np.max(pos_neg_shear_z, axis=0)
        v_rd = self.get_shear_force_resistance()

        self.shear_check[envelope] = ShearCheck(
            v_ed=shear_z,
            v_rd=v_rd
        )

    def perform_bending_checks_envelope(self, envelope: EnvelopeCombination) -> None:
        pos_bending_y, neg_bending_y = self.member.results.bending_moments_y.get(envelope)

        m_rd_positive, m_rd_negative = self.get_moments_of_resistance()

        self.bending_check[envelope] = (
            [
                BendingCheck(
                    m_ed=pos_bending_y,
                    m_rd_positive=m_rd_positive,
                    m_rd_negative=m_rd_negative,
                ),
                BendingCheck(
                    m_ed=neg_bending_y,
                    m_rd_positive=m_rd_positive,
                    m_rd_negative=m_rd_negative,
                )
            ]
        )



if __name__ == "__main__":
    import math
    from framesss.solvers.linear_static import LinearStaticSolver

    from desssign.concrete.concrete_material import ConcreteMaterial
    from desssign.concrete.concrete_section import ConcreteSection
    from desssign.common.model import DesignModelFrameXZ

    material = ConcreteMaterial(strength_class="C20/25")
    sectionA = ConcreteSection(
        label="FOO",
        points=[[0.0, 0.0], [0.3, 0.0], [0.3, 0.5], [0.0, 0.5]],
        material=material,
        v_rd=60e3,
        m_rd_positive=30e3,
        m_rd_negative=-40e3,
    )
    sectionB = ConcreteSection(
        label="FOO",
        points=[[0.0, 0.0], [0.6, 0.0], [0.6, 1.0], [0.0, 1.0]],
        material=material,
        v_rd=120e3,
        m_rd_positive=60e3,
        m_rd_negative=-80e3,
    )

    model = DesignModelFrameXZ()

    fixed = ["fixed", "free", "fixed", "free", "fixed", "free"]
    vertical_roller = ["fixed", "free", "free", "free", "free", "free"]

    node_1 = model.add_node("1", [0, 0, 0], fixity=fixed)
    node_2 = model.add_node("2", [6, 0, 0], fixity=fixed)

    member_12 = model.add_concrete_member(
        label="1-2",
        element_type="navier",
        nodes=[node_1, node_2],
        section=sectionA
    )

    member_12.define_sections(
        sections={
            (0.0, 3.0): sectionA,
            (3.0, 6.0): sectionB
        }
    )

    lc1 = model.add_design_load_case(
        label="LC1",
        load_type="variable",
        category="a",
    )

    member_12.add_distributed_load(
        load_components=np.array([0, 0, 25, 0, 0, 25]) * 1e3,
        load_case=lc1
    )

    lc2 = model.add_design_load_case(
        label="LC2",
        load_type="permanent",
    )

    member_12.add_distributed_load(
        load_components=np.array([0, 0, 50, 0, 0, 50]) * 1e3,
        load_case=lc2
    )

    comb1 = model.add_design_load_case_combination(
        label="CO1",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=lc1,
        other_variable_cases=[],
    )

    comb2 = model.add_design_load_case_combination(
        label="CO1",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=None,
        other_variable_cases=[],
    )

    env = model.add_envelope(
        label="ULS",
        cases=[comb1, comb2]
    )

    solver = LinearStaticSolver(model)
    solver.solve()

    model.perform_uls_checks(envelope=env)

    print("")
