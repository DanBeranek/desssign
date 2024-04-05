from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

from desssign.loads.enums import LimitState
from desssign.loads.enums import LoadType
from desssign.loads.enums import SLSCombination
from desssign.loads.enums import ULSCombination
from desssign.loads.load_combination_generator.generate_combinations import (
    generate_combination,
)
from desssign.utils import flatten_list

if TYPE_CHECKING:
    from desssign.loads.load_case_group import LoadCaseGroup
    from desssign.loads.load_combination import DesignLoadCaseCombination


class CombinationsGenerator:
    """
    A class used to generate all possible combinations of load cases for a specific limit state.

    :ivar limit_state: The limit state of the combination group. Either ULS or SLS.
    :ivar combination_type: The type of the combination group. For ULS: basic, alternative or accidental,
                            for SLS: characteristic, frequent or quasi-permanent.
    :ivar combinations: A list of all generated combinations of load cases.
    """

    def __init__(
        self,
        limit_state: str | LimitState,
        combination_type: str | SLSCombination | ULSCombination,
    ) -> None:
        """
        Initialize the CombinationsGenerator class.

        :param limit_state: The limit state of the combination group. Either ULS or SLS.
        :type limit_state: str | LimitState
        :param combination_type: The type of the combination group. For ULS: basic, alternative or accidental,
                                 for SLS: characteristic, frequent or quasi-permanent.
        :type combination_type: str | SLSCombination | ULSCombination
        :raises AttributeError: If the combination type does not match the limit state.
        """
        self.limit_state = LimitState(limit_state)

        if self.limit_state == LimitState.ULS:
            self.combination_type = ULSCombination(combination_type)
        elif self.limit_state == LimitState.SLS:
            self.combination_type = SLSCombination(combination_type)
        else:
            raise AttributeError(
                f"Can't set combination type: '{combination_type}' to limit state: '{limit_state}'."
            )

        self.combinations: list[DesignLoadCaseCombination] = []

    def generate_combinations(self, *args: list[LoadCaseGroup]) -> None:
        """
        Generate all possible combinations of load cases.

        :param args: Variable length argument list of LoadCaseGroup lists.
        :type args: list[LoadCaseGroup]
        """
        # get all possible combinations
        all_iterables = []
        for load_groups in args:
            all_iterables.append(
                [load_group.combinations for load_group in load_groups]
            )

        combinations = []
        for iterables in all_iterables:
            combinations.extend(
                [flatten_list(combination) for combination in product(*iterables)]
            )

        # get all possible unique combinations
        unique_combinations = []
        for combination in combinations:
            if combination not in unique_combinations:
                unique_combinations.append(combination)

        c = 0
        for unique_combination in unique_combinations:
            permanent_cases = [
                case
                for case in unique_combination
                if case.load_type == LoadType.PERMANENT
            ]
            variable_cases = [
                case
                for case in unique_combination
                if case.load_type == LoadType.VARIABLE
            ]

            if variable_cases:
                for i, leading_variable_case in enumerate(variable_cases):
                    # loop through every possible combination of leading + other variable for this unique combination
                    other_variable_cases = variable_cases[:i] + variable_cases[i + 1 :]

                    self.combinations.extend(
                        generate_combination(
                            c,
                            permanent_cases,
                            leading_variable_case,
                            other_variable_cases,
                            self.combination_type,
                        )
                    )

                    c += 1
            else:  # in case there is only permanent cases
                self.combinations.extend(
                    generate_combination(
                        c, permanent_cases, None, [], self.combination_type
                    )
                )
                c += 1


if __name__ == "__main__":
    from desssign.loads.load_case import DesignLoadCase
    from desssign.loads.load_case_group import LoadCaseGroup

    G1 = DesignLoadCase("G1", "permanent")
    G2 = DesignLoadCase("G2", "permanent")
    LG1 = LoadCaseGroup([G1, G2], "together")

    Q1 = DesignLoadCase("Q1", "variable", "category a")
    Q2 = DesignLoadCase("Q2", "variable", "category b")
    LG2 = LoadCaseGroup([Q1, Q2], "standard")

    S1 = DesignLoadCase("S1", "variable", "snow < 1000 m")
    S2 = DesignLoadCase("S2", "variable", "snow < 1000 m")
    S3 = DesignLoadCase("S3", "variable", "snow < 1000 m")
    LG3 = LoadCaseGroup([S1, S2, S3], "exclusive")

    W1 = DesignLoadCase("W1", "variable", "wind")
    W2 = DesignLoadCase("W2", "variable", "wind")
    W3 = DesignLoadCase("W3", "variable", "wind")
    W4 = DesignLoadCase("W4", "variable", "wind")
    LG4 = LoadCaseGroup([W1, W2, W3, W4], "exclusive")

    ULS = CombinationsGenerator("ULS", "basic")

    ULS.generate_combinations([LG1, LG2], [LG1, LG3, LG4])

    for comb in ULS.combinations:
        print(comb.combination_key)

    print("")
