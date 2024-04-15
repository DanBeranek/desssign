import pytest

from desssign.loads.enums import LoadCaseRelation
from desssign.loads.enums import LoadDurationClass
from desssign.loads.enums import LoadType
from desssign.loads.enums import VariableCategory
from desssign.loads.load_case import DesignLoadCase
from desssign.loads.load_case_group import DesignLoadCaseGroup


@pytest.fixture
def load_cases() -> list[DesignLoadCase]:
    return [
        DesignLoadCase(
            label=f"lc{i}",
            load_type=LoadType.VARIABLE,
            category=VariableCategory.C,
            load_duration_class=LoadDurationClass.MEDIUM_TERM,
        )
        for i in range(3)
    ]


def test_init(load_cases) -> None:
    load_case_group = DesignLoadCaseGroup(load_cases, LoadCaseRelation.STANDARD)
    assert load_case_group.load_cases == load_cases
    assert load_case_group.load_case_relation == LoadCaseRelation.STANDARD


def test_number_of_load_cases(load_cases) -> None:
    load_case_group = DesignLoadCaseGroup(load_cases, LoadCaseRelation.STANDARD)
    assert load_case_group.number_of_load_cases == len(load_cases)


def test_standard_relation(load_cases) -> None:
    load_case_group = DesignLoadCaseGroup(load_cases, LoadCaseRelation.STANDARD)
    assert len(load_case_group.combinations) == 2 ** len(load_cases)
    assert load_case_group.combinations[0] == []
    assert load_case_group.combinations[1] == [load_cases[0]]
    assert load_case_group.combinations[2] == [load_cases[1]]
    assert load_case_group.combinations[3] == [load_cases[2]]
    assert load_case_group.combinations[4] == [load_cases[0], load_cases[1]]
    assert load_case_group.combinations[5] == [load_cases[0], load_cases[2]]
    assert load_case_group.combinations[6] == [load_cases[1], load_cases[2]]
    assert load_case_group.combinations[7] == load_cases


def test_together_relation(load_cases) -> None:
    load_case_group = DesignLoadCaseGroup(load_cases, LoadCaseRelation.TOGETHER)
    assert len(load_case_group.combinations) == 1
    assert load_case_group.combinations == [load_cases]


def test_exclusive_relation(load_cases) -> None:
    load_case_group = DesignLoadCaseGroup(load_cases, LoadCaseRelation.EXCLUSIVE)
    assert len(load_case_group.combinations) == len(load_cases) + 1
    assert load_case_group.combinations[0] == []
    assert load_case_group.combinations[1] == [load_cases[0]]
    assert load_case_group.combinations[2] == [load_cases[1]]
    assert load_case_group.combinations[3] == [load_cases[2]]


def test_invalid_relation(load_cases) -> None:
    with pytest.raises(ValueError):
        load_case_group = DesignLoadCaseGroup(load_cases, "invalid_relation")
        _ = load_case_group.combinations
