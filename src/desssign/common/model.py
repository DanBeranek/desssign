from __future__ import annotations

from typing import TYPE_CHECKING

from framesss.enums import BeamConnection
from framesss.enums import Element1DType
from framesss.fea.analysis.analysis import Analysis
from framesss.fea.analysis.frame_xz_analysis import FrameXZAnalysis
from framesss.fea.models.model import Model

from desssign.loads.enums import LimitState
from desssign.loads.enums import LoadDurationClass
from desssign.loads.enums import LoadType
from desssign.loads.enums import SLSCombination
from desssign.loads.enums import ULSAlternativeCombination
from desssign.loads.enums import ULSCombination
from desssign.loads.enums import VariableCategory
from desssign.loads.load_case import DesignLoadCase
from desssign.loads.load_case_combination import DesignNonlinearLoadCaseCombination
from desssign.loads.load_case_combination import DesignLoadCaseCombination

from desssign.wood.wood_member import WoodMember1D
from desssign.concrete.concrete_member import ConcreteMember1D

if TYPE_CHECKING:
    from framesss.fea.node import Node

    from desssign.wood.wood_section import WoodRectangularSection
    from desssign.concrete.concrete_section import ConcreteSection


class DesignModel(Model):
    """
    Class represent the entire structural analysis model.

    Upon :class:`framesss.fea.models.Model` class, it changes
    """
    load_combinations: set[DesignLoadCaseCombination]
    nonlinear_load_combinations: set[DesignNonlinearLoadCaseCombination]
    members: set[WoodMember1D | ConcreteMember1D]

    def __init__(self, analysis: Analysis) -> None:
        """Init the DesignModel object."""
        super().__init__(analysis)

    def add_wood_member(
        self,
        label: str,
        element_type: str,
        nodes: list[Node],
        section: WoodRectangularSection,
        hinges: list[str] | tuple[str, str] = (BeamConnection.CONTINUOUS_END,) * 2,
    ) -> WoodMember1D:
        """
        Create and return new :class:`WoodMember1D` instance.

        :param label: A user-defined label for the member.
        :param element_type: Specifies the type of the element ('navier', 'timoshenko').
        :param nodes: A list of nodes at the start and the end of the member.
        :param section: The cross-section of the member.
        :param hinges: Defines the type of connections at the start and the end of the  member
                       (e.g., fixed, hinged, or semirigid) to model the rotational stiffness accurately.
        """
        elem_type = Element1DType(element_type)
        hngs = [BeamConnection(hng) for hng in hinges]

        aux = self.analysis.get_auxiliary_vector_in_local_xy_plane(nodes)
        new_member = WoodMember1D(
            label,
            elem_type,
            nodes,
            section,
            hngs,
            aux,
            self.analysis,
        )
        self.members.add(new_member)
        return new_member

    def add_concrete_member(
        self,
        label: str,
        element_type: str,
        nodes: list[Node],
        section: ConcreteSection,
        hinges: list[str] | tuple[str, str] = (BeamConnection.CONTINUOUS_END,) * 2,
    ) -> ConcreteMember1D:
        """
        Create and return new :class:`ConcreteMember1D` instance.

        :param label: A user-defined label for the member.
        :param element_type: Specifies the type of the element ('navier', 'timoshenko').
        :param nodes: A list of nodes at the start and the end of the member.
        :param section: The cross-section of the member.
        :param hinges: Defines the type of connections at the start and the end of the  member
                       (e.g., fixed, hinged, or semirigid) to model the rotational stiffness accurately.
        """
        elem_type = Element1DType(element_type)
        hngs = [BeamConnection(hng) for hng in hinges]

        aux = self.analysis.get_auxiliary_vector_in_local_xy_plane(nodes)
        new_member = ConcreteMember1D(
            label,
            elem_type,
            nodes,
            section,
            hngs,
            aux,
            self.analysis,
        )
        self.members.add(new_member)
        return new_member

    def add_design_load_case(
        self,
        label: str,
        description: str = "",
        load_type: str | LoadType = LoadType.PERMANENT,
        category: str | VariableCategory | None = None,
        load_duration_class: str | LoadDurationClass = LoadDurationClass.PERMANENT,
    ) -> DesignLoadCase:
        """
        Add and return new :class:`DesignLoadCase` instance.

        :param label: Unique user-defined label of the load case.
        :param description: A description of the load case.
        :param load_type: The type of the load case. Either 'permanent', 'variable' or 'accidental'.
        :param category: The category of the variable load case. Only required for variable load cases.
        :param load_duration_class: The load duration class of the load case.
        """
        load_type = LoadType(load_type)
        category = VariableCategory(category) if category is not None else None
        load_duration_class = (
            LoadDurationClass(load_duration_class)
            if load_duration_class is not None
            else None
        )
        if load_type == LoadType.VARIABLE and category is None:
            raise ValueError("Variable load cases require a category.")
        if load_duration_class is None:
            raise ValueError("Load duration class must be provided.")

        new_case = DesignLoadCase(
            label, load_type, category, load_duration_class, description
        )
        self.load_cases.add(new_case)
        return new_case

    def add_design_load_case_combination(
        self,
        label: str,
        limit_state: str | LimitState,
        combination_type: str | SLSCombination | ULSCombination,
        permanent_cases: list[DesignLoadCase],
        leading_variable_case: DesignLoadCase | None,
        other_variable_cases: list[DesignLoadCase],
        is_nonlinear: bool = False,
    ) -> (
        DesignLoadCaseCombination |
        DesignNonlinearLoadCaseCombination |
        tuple[DesignLoadCaseCombination, DesignLoadCaseCombination] |
        tuple[DesignNonlinearLoadCaseCombination, DesignNonlinearLoadCaseCombination]
    ):
        """
        Add and return new :class:`LoadCaseCombination` instance.

        :param label: The label of the load case combination.
        :param limit_state: The limit state of the combination group. Either 'ULS' or 'SLS'.
        :param combination_type: The type of the combination group. For ULS: basic, alternative or accidental,
                                 for SLS: characteristic, frequent or quasi-permanent.
        :param permanent_cases: A list of permanent load cases.
        :param leading_variable_case: The leading variable load case.
        :param other_variable_cases: A list of other variable load cases.
        :param is_nonlinear: Flag if the combination is nonlinear.
        """
        CombinationClass = DesignNonlinearLoadCaseCombination if is_nonlinear else DesignLoadCaseCombination
        if combination_type == ULSCombination.ALTERNATIVE:
            new_combination_a = CombinationClass(
                label=f"{label}(a)",
                limit_state=limit_state,
                combination_type=combination_type,
                permanent_cases=permanent_cases,
                leading_variable_case=leading_variable_case,
                other_variable_cases=other_variable_cases,
                alternative_combination=ULSAlternativeCombination.REDUCED_VARIABLE,
            )

            new_combination_b = CombinationClass(
                label=f"{label}(b)",
                limit_state=limit_state,
                combination_type=combination_type,
                permanent_cases=permanent_cases,
                leading_variable_case=leading_variable_case,
                other_variable_cases=other_variable_cases,
                alternative_combination=ULSAlternativeCombination.REDUCED_PERMANENT,
            )

            if is_nonlinear:
                self.nonlinear_load_combinations.add(new_combination_a)
                self.nonlinear_load_combinations.add(new_combination_b)
            else:
                self.load_combinations.add(new_combination_a)
                self.load_combinations.add(new_combination_b)
            return new_combination_a, new_combination_b

        new_combination = CombinationClass(
            label=label,
            limit_state=limit_state,
            combination_type=combination_type,
            permanent_cases=permanent_cases,
            leading_variable_case=leading_variable_case,
            other_variable_cases=other_variable_cases,
        )
        if is_nonlinear:
            self.nonlinear_load_combinations.add(new_combination)
        else:
            self.load_combinations.add(new_combination)
        return new_combination

    def perform_uls_checks(self) -> None:
        """Perform ULS checks on the model members."""
        combinations = [
            comb
            for comb in self.load_combinations.union(
                self.nonlinear_load_combinations
            ) if comb.limit_state == LimitState.ULS
        ]

        for member in self.members:
            member.perform_uls_checks(combinations)


class DesignModelFrameXZ(DesignModel):
    """
    Class represent the entire structural analysis model.
    """

    def __init__(self) -> None:
        """Init the DesignModelFrameXZ object."""
        super().__init__(FrameXZAnalysis())
