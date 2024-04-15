from __future__ import annotations

import pytest

from desssign.loads.enums import LimitState
from desssign.loads.enums import LoadCaseRelation
from desssign.loads.enums import LoadDurationClass
from desssign.loads.enums import LoadType
from desssign.loads.enums import ULSCombination
from desssign.loads.enums import VariableCategory
from desssign.loads.load_case import DesignLoadCase
from desssign.loads.load_case_combination import DesignLoadCaseCombination
from desssign.loads.load_case_group import DesignLoadCaseGroup
from desssign.loads.load_combination_generator.combination_generator import CombinationsGenerator


@pytest.fixture
def permanent_load_case_group() -> DesignLoadCaseGroup:
    load_cases = [
        DesignLoadCase(
            label=f"G{i}",
            load_type=LoadType.PERMANENT,
            category=None,
            load_duration_class=LoadDurationClass.PERMANENT,
        )
        for i in range(4)
    ]
    return DesignLoadCaseGroup(load_cases, LoadCaseRelation.TOGETHER)


@pytest.fixture
def imposed_load_case_group() -> DesignLoadCaseGroup:
    load_cases = [
        DesignLoadCase(
            label=f"Q{i}",
            load_type=LoadType.VARIABLE,
            category=VariableCategory.C,
            load_duration_class=LoadDurationClass.MEDIUM_TERM,
        )
        for i in range(3)
    ]
    return DesignLoadCaseGroup(load_cases, LoadCaseRelation.STANDARD)


@pytest.fixture
def wind_load_case_group() -> DesignLoadCaseGroup:
    load_cases = [
        DesignLoadCase(
            label=f"W{i}",
            load_type=LoadType.VARIABLE,
            category=VariableCategory.WIND,
            load_duration_class=LoadDurationClass.SHORT_TERM,
        )
        for i in range(4)
    ]
    return DesignLoadCaseGroup(load_cases, LoadCaseRelation.EXCLUSIVE)


def test_init(permanent_load_case_group: DesignLoadCaseGroup) -> None:
    combinations_generator = CombinationsGenerator(LimitState.ULS, ULSCombination.BASIC)
    assert combinations_generator.limit_state == LimitState.ULS
    assert combinations_generator.combination_type == ULSCombination.BASIC
    assert combinations_generator.combinations == []


def test_generate_combinations_basic(
    permanent_load_case_group: DesignLoadCaseGroup,
    imposed_load_case_group: DesignLoadCaseGroup,
    wind_load_case_group: DesignLoadCaseGroup,
) -> None:
    combinations_generator = CombinationsGenerator(LimitState.ULS, ULSCombination.BASIC)
    combinations_generator.generate_combinations(
        [
            permanent_load_case_group,
            imposed_load_case_group,
            wind_load_case_group,
        ]
    )
    assert len(combinations_generator.combinations) > 0

    combination_keys = []
    combination_cases = []
    for combination in combinations_generator.combinations:
        assert isinstance(combination, DesignLoadCaseCombination)
        assert combination.limit_state == LimitState.ULS
        assert combination.combination_type == ULSCombination.BASIC
        assert combination.permanent_cases == permanent_load_case_group.load_cases
        assert (
            combination.leading_variable_case
            in imposed_load_case_group.load_cases
            + wind_load_case_group.load_cases
            + [None]
        )

        # Check that each combination key is unique
        assert combination.combination_key not in combination_keys
        combination_keys.append(combination.combination_key)

        # Check that each combination of cases is unique
        cases = (
            combination.permanent_cases,
            combination.leading_variable_case,
            combination.other_variable_cases,
        )
        assert cases not in combination_cases
        combination_cases.append(cases)

        # Check that there are all permanent load cases in the combination
        assert all(
            case in combination.load_cases
            for case in permanent_load_case_group.load_cases
        )

        # Check that there are 0 or 1 wind load cases in the combination
        wind_cases = [
            case
            for case in combination.load_cases
            if case in wind_load_case_group.load_cases
        ]
        assert len(wind_cases) in [0, 1]

        # Check that there are 0 to n imposed load cases in the combination
        imposed_cases = [
            case
            for case in combination.load_cases
            if case in imposed_load_case_group.load_cases
        ]
        assert len(imposed_cases) in range(len(imposed_load_case_group.load_cases) + 1)


def test_generate_combinations_alternative(
    permanent_load_case_group: DesignLoadCaseGroup,
    imposed_load_case_group: DesignLoadCaseGroup,
    wind_load_case_group: DesignLoadCaseGroup,
) -> None:
    combinations_generator = CombinationsGenerator(
        LimitState.ULS, ULSCombination.ALTERNATIVE
    )
    combinations_generator.generate_combinations(
        [
            permanent_load_case_group,
            imposed_load_case_group,
            wind_load_case_group,
        ]
    )
    assert len(combinations_generator.combinations) > 0

    combination_keys = []
    combination_cases: dict[
        tuple[
            tuple[DesignLoadCase, ...],
            DesignLoadCase | None,
            tuple[DesignLoadCase, ...],
        ],
        int,
    ] = {}
    for combination in combinations_generator.combinations:
        assert isinstance(combination, DesignLoadCaseCombination)
        assert combination.limit_state == LimitState.ULS
        assert combination.combination_type == ULSCombination.ALTERNATIVE
        assert combination.permanent_cases == permanent_load_case_group.load_cases
        assert (
            combination.leading_variable_case
            in imposed_load_case_group.load_cases
            + wind_load_case_group.load_cases
            + [None]
        )

        # Check that each combination key is unique
        assert combination.combination_key not in combination_keys
        combination_keys.append(combination.combination_key)

        # Check that each combination of cases appears twice
        cases = (
            tuple(combination.permanent_cases),
            combination.leading_variable_case,
            tuple(combination.other_variable_cases),
        )
        if cases in combination_cases:
            combination_cases[cases] += 1
        else:
            combination_cases[cases] = 1

    for count in combination_cases.values():
        assert count == 2

    # Check that there are twice as many combinations as in the basic scenario
    combinations_generator_basic = CombinationsGenerator(
        LimitState.ULS, ULSCombination.BASIC
    )
    combinations_generator_basic.generate_combinations(
        [
            permanent_load_case_group,
            imposed_load_case_group,
            wind_load_case_group,
        ]
    )
    assert len(combinations_generator.combinations) == 2 * len(
        combinations_generator_basic.combinations
    )
