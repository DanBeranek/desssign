from __future__ import annotations
from typing import TYPE_CHECKING

from desssign.loads.load_combination import DesignLoadCombination
from desssign.loads.load_combination_generator.constants import PSI_FACTORS, GAMMA_VALUES, XI
from desssign.loads.enums import LoadBehavior
from desssign.loads.enums import SLSCombination, ULSCombination

if TYPE_CHECKING:
    from desssign.loads.load_case import DesignLoadCase


def generate_combination(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase],
    combination: SLSCombination | ULSCombination
) -> list[DesignLoadCombination]:
    if combination == SLSCombination.CHARACTERISTIC:
        return generate_sls_characteristic_combination(i, permanent_cases, leading_variable_case, other_variable_cases)

    if combination == SLSCombination.FREQUENT:
        return generate_sls_frequent_combination(i, permanent_cases, leading_variable_case, other_variable_cases)

    if combination == SLSCombination.QUASIPERMANENT:
        return generate_sls_quasipermanent_combination(i, permanent_cases, leading_variable_case, other_variable_cases)

    if combination == ULSCombination.BASIC:
        return generate_uls_basic_combination(i, permanent_cases, leading_variable_case, other_variable_cases)

    if combination == ULSCombination.ALTERNATIVE:
        return generate_uls_alternative_combinations(i, permanent_cases, leading_variable_case, other_variable_cases)


def generate_sls_characteristic_combination(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase]
) -> list[DesignLoadCombination]:
    cases = {}
    key = ""

    for case in permanent_cases:
        cases[case] = 1.
        key += case.label + "+"

    if leading_variable_case is not None:
        cases[leading_variable_case] = 1.
        key += leading_variable_case.label + "+"

    for case in other_variable_cases:
        factor = PSI_FACTORS[case.category]["psi_0"]
        cases[case] = factor
        key += str(factor) + "*" + case.label
        if case != other_variable_cases[-1]:
            key += "+"

    return [DesignLoadCombination(f"SLS-Characteristic-{i}", cases, key)]


def generate_sls_frequent_combination(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase]
) -> list[DesignLoadCombination]:
    cases = {}
    key = ""

    for case in permanent_cases:
        cases[case] = 1.
        key += case.label + "+"

    if leading_variable_case is not None:
        factor = PSI_FACTORS[leading_variable_case.category]["psi_1"]
        cases[leading_variable_case] = factor
        key += str(factor) + "*" + leading_variable_case.label + "+"

    for case in other_variable_cases:
        factor = PSI_FACTORS[case.category]["psi_2"]
        cases[case] = factor
        key += str(factor) + "*" + case.label
        if case != other_variable_cases[-1]:
            key += "+"

    return [DesignLoadCombination(f"SLS-Frequent-{i}", cases, key)]


def generate_sls_quasipermanent_combination(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase]
) -> list[DesignLoadCombination]:
    cases = {}
    key = ""

    for case in permanent_cases:
        cases[case] = 1.
        key += case.label + "+"

    if leading_variable_case is not None:
        factor = PSI_FACTORS[leading_variable_case.category]["psi_2"]
        cases[leading_variable_case] = factor
        key += str(factor) + "*" + leading_variable_case.label + "+"

    for case in other_variable_cases:
        factor = PSI_FACTORS[case.category]["psi_2"]
        cases[case] = factor
        key += str(factor) + "*" + case.label
        if case != other_variable_cases[-1]:
            key += "+"

    return [DesignLoadCombination(f"SLS-Frequent-{i}", cases, key)]


def generate_uls_basic_combination(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase]
) -> list[DesignLoadCombination]:
    cases = {}
    key = ""

    for case in permanent_cases:
        factor = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        cases[case] = factor
        key += f"{factor}*{case.label}+"

    if leading_variable_case is not None:
        factor = GAMMA_VALUES["Set B"][leading_variable_case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        cases[leading_variable_case] = factor
        key += f"{factor}*{leading_variable_case.label}+"

    for case in other_variable_cases:
        gamma = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        psi = PSI_FACTORS[case.category]["psi_0"]
        cases[case] = gamma * psi
        key += f"{gamma}*{psi}*{case.label}"
        if case != other_variable_cases[-1]:
            key += "+"

    return [DesignLoadCombination(f"ULS-Basic(6.10)-{i}", cases, key)]


def generate_uls_alternative_combinations(
    i: int,
    permanent_cases: list[DesignLoadCase],
    leading_variable_case: DesignLoadCase | None,
    other_variable_cases: list[DesignLoadCase]
) -> list[DesignLoadCombination]:
    cases_a = {}
    key_a = ""

    for case in permanent_cases:
        gamma = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        cases_a[case] = gamma
        key_a += f"{gamma}*{case.label}+"

    if leading_variable_case is not None:
        gamma = GAMMA_VALUES["Set B"][leading_variable_case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        psi = PSI_FACTORS[leading_variable_case.category]["psi_0"]
        cases_a[leading_variable_case] = gamma * psi
        key_a += f"{gamma}*{psi}*{leading_variable_case.label}+"

    for case in other_variable_cases:
        gamma = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        psi = PSI_FACTORS[case.category]["psi_0"]
        cases_a[case] = gamma * psi
        key_a += f"{gamma}*{psi}*{case.label}"
        if case != other_variable_cases[-1]:
            key_a += "+"

    cases_b = {}
    key_b = ""

    for case in permanent_cases:
        gamma = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        cases_b[case] = gamma * XI
        key_b += f"{XI}*{gamma}*{case.label}+"

    if leading_variable_case is not None:
        gamma = GAMMA_VALUES["Set B"][leading_variable_case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        cases_b[leading_variable_case] = gamma
        key_b += f"{gamma}*{leading_variable_case.label}+"

    for case in other_variable_cases:
        gamma = GAMMA_VALUES["Set B"][case.load_type][LoadBehavior.UNFAVOURABLE]  # TODO: Favourable?
        psi = PSI_FACTORS[case.category]["psi_0"]
        cases_b[case] = gamma * psi
        key_b += f"{gamma}*{psi}*{case.label}"
        if case != other_variable_cases[-1]:
            key_b += "+"

    combinations = [
        DesignLoadCombination(f"ULS-Alternative(6.10a)-{i}", cases_a, key_a),
        DesignLoadCombination(f"ULS-Alternative(6.10b)-{i}", cases_b, key_b)
    ]

    return combinations
