import pytest

from desssign.loads.enums import LimitState
from desssign.loads.enums import LoadDurationClass
from desssign.loads.enums import LoadType
from desssign.loads.enums import ULSCombination
from desssign.loads.enums import VariableCategory
from desssign.loads.load_case import DesignLoadCase
from desssign.loads.load_case_combination import DesignLoadCaseCombination


@pytest.fixture
def permanent_cases() -> list[DesignLoadCase]:
    return [
        DesignLoadCase(
            label="G1",
            load_type=LoadType.PERMANENT,
            category=None,
            load_duration_class=LoadDurationClass.PERMANENT,
        )
    ]


@pytest.fixture
def leading_variable_case() -> DesignLoadCase:
    return DesignLoadCase(
        label="Q2",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.C,
        load_duration_class=LoadDurationClass.MEDIUM_TERM,
    )


@pytest.fixture
def other_variable_cases() -> list[DesignLoadCase]:
    return [
        DesignLoadCase(
            label="Q3",
            load_type=LoadType.VARIABLE,
            category=VariableCategory.WIND,
            load_duration_class=LoadDurationClass.SHORT_TERM,
        )
    ]


@pytest.fixture
def combination(
    permanent_cases, leading_variable_case, other_variable_cases
) -> DesignLoadCaseCombination:
    return DesignLoadCaseCombination(
        label="comb",
        limit_state=LimitState.ULS,
        combination_type=ULSCombination.BASIC,
        permanent_cases=permanent_cases,
        leading_variable_case=leading_variable_case,
        other_variable_cases=other_variable_cases,
    )


def test_init(
    combination, leading_variable_case, permanent_cases, other_variable_cases
) -> None:
    assert combination.limit_state == LimitState.ULS
    assert combination.combination_type == ULSCombination.BASIC
    assert combination.permanent_cases == permanent_cases
    assert combination.leading_variable_case == leading_variable_case
    assert combination.other_variable_cases == other_variable_cases


def test_invalid_limit_state(permanent_cases, other_variable_cases) -> None:
    with pytest.raises(ValueError):
        DesignLoadCaseCombination(
            label="comb",
            limit_state="invalid",
            combination_type=ULSCombination.BASIC,
            permanent_cases=permanent_cases,
            leading_variable_case=None,
            other_variable_cases=other_variable_cases,
        )


def test_invalid_alternative_combination(permanent_cases, other_variable_cases) -> None:
    with pytest.raises(ValueError):
        DesignLoadCaseCombination(
            label="comb",
            limit_state=LimitState.ULS,
            combination_type=ULSCombination.ALTERNATIVE,
            permanent_cases=permanent_cases,
            leading_variable_case=None,
            other_variable_cases=other_variable_cases,
            alternative_combination=None,
        )


def test_get_combination(
    combination, leading_variable_case, permanent_cases, other_variable_cases
) -> None:
    load_cases, combination_key = combination._get_combination()
    assert load_cases[permanent_cases[0]] == pytest.approx(1.35, abs=1e-9)
    assert load_cases[leading_variable_case] == pytest.approx(1.5, abs=1e-9)
    assert load_cases[other_variable_cases[0]] == pytest.approx(0.9, abs=1e-9)
    assert combination_key == "1.35*G1+1.5*Q2+1.5*0.6*Q3"


def test_load_duration_class() -> None:
    lc1 = DesignLoadCase(
        label="lc1",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.C,
        load_duration_class=LoadDurationClass.MEDIUM_TERM,
    )

    lc2 = DesignLoadCase(
        label="lc2",
        load_type=LoadType.PERMANENT,
        load_duration_class=LoadDurationClass.PERMANENT,
    )

    lc3 = DesignLoadCase(
        label="lc3",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.WIND,
        load_duration_class=LoadDurationClass.INSTANTANEOUS,
    )

    lc4 = DesignLoadCase(
        label="lc4",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.SNOW_BELLOW_1000_M,
        load_duration_class=LoadDurationClass.SHORT_TERM,
    )

    comb_medium = DesignLoadCaseCombination(
        label="comb",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=lc1,
        other_variable_cases=[],
    )

    comb_permanent = DesignLoadCaseCombination(
        label="comb",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=None,
        other_variable_cases=[],
    )

    comb_short = DesignLoadCaseCombination(
        label="comb",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=lc1,
        other_variable_cases=[lc4],
    )

    comb_inst = DesignLoadCaseCombination(
        label="comb",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2],
        leading_variable_case=lc1,
        other_variable_cases=[lc3, lc4],
    )

    assert comb_medium.load_duration_class == LoadDurationClass.MEDIUM_TERM
    assert comb_permanent.load_duration_class == LoadDurationClass.PERMANENT
    assert comb_short.load_duration_class == LoadDurationClass.SHORT_TERM
    assert comb_inst.load_duration_class == LoadDurationClass.INSTANTANEOUS
