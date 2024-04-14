from desssign.loads.enums import LoadType, LoadDurationClass
from desssign.loads.enums import VariableCategory

from desssign.loads.load_case import DesignLoadCase
from desssign.loads.load_combination import DesignLoadCaseCombination


def test_load_duration_class_for_combinations() -> None:
    lc1 = DesignLoadCase(
        label="lc1",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.C,
        load_duration_class=LoadDurationClass.MEDIUM_TERM
    )

    lc2 = DesignLoadCase(
        label="lc2",
        load_type=LoadType.PERMANENT,
        load_duration_class=LoadDurationClass.PERMANENT
    )

    lc3 = DesignLoadCase(
        label="lc3",
        load_type=LoadType.ACCIDENTAL,
        load_duration_class=LoadDurationClass.INSTANTANEOUS
    )

    lc4 = DesignLoadCase(
        label="lc4",
        load_type=LoadType.VARIABLE,
        category=VariableCategory.SNOW_BELLOW_1000_M,
        load_duration_class=LoadDurationClass.SHORT_TERM
    )

    comb_medium = DesignLoadCaseCombination(
        label="comb",
        load_cases={lc1: 1.0, lc2: 1.0},
        combination_key="comb"
    )

    comb_permanent = DesignLoadCaseCombination(
        label="comb",
        load_cases={lc2: 1.0},
        combination_key="comb"
    )

    comb_short = DesignLoadCaseCombination(
        label="comb",
        load_cases={lc1: 1.0, lc2: 1.0, lc4: 1.0},
        combination_key="comb"
    )

    comb_inst = DesignLoadCaseCombination(
        label="comb",
        load_cases={lc1: 1.0, lc2: 1.0, lc3:1.0, lc4: 1.0},
        combination_key="comb"
    )

    assert comb_medium.load_duration_class == LoadDurationClass.MEDIUM_TERM
    assert comb_permanent.load_duration_class == LoadDurationClass.PERMANENT
    assert comb_short.load_duration_class == LoadDurationClass.SHORT_TERM
    assert comb_inst.load_duration_class == LoadDurationClass.INSTANTANEOUS
