from __future__ import annotations
from typing import TYPE_CHECKING

from itertools import product

from desssign.loads.enums import LimitState, LoadType
from desssign.loads.enums import SLSCombination, ULSCombination
from desssign.utils import flatten_list
from desssign.loads.load_combination_generator.generate_combinations import generate_combination

if TYPE_CHECKING:
    from desssign.loads.load_combination import DesignLoadCombination
    from desssign.loads.load_group import LoadGroup


class CombinationGroup:
    def __init__(self,
                 limit_state: str | LimitState,
                 combination_type: str | SLSCombination | ULSCombination) -> None:
        """Init the CombinationGroup class."""
        self.limit_state = LimitState(limit_state)

        if self.limit_state == LimitState.ULS:
            self.combination_type = ULSCombination(combination_type)
        elif self.limit_state == LimitState.SLS:
            self.combination_type = SLSCombination(combination_type)
        else:
            raise AttributeError(f"Can't set combination type: '{combination_type}' to limit state: '{limit_state}'.")

        self.combinations: list[DesignLoadCombination] = []

    def generate_combinations(self, *args: LoadGroup) -> None:
        # TODO: Duplicates permanent load cases when multiple generate combinations is called
        # get all possible combinations
        iterables = [load_group.combinations for load_group in args]

        # get all possible unique combinations
        unique_combinations = [flatten_list(combination) for combination in product(*iterables)]

        c = 0
        for unique_combination in unique_combinations:
            permanent_cases = [case for case in unique_combination if case.load_type == LoadType.PERMANENT]
            variable_cases = [case for case in unique_combination if case.load_type == LoadType.VARIABLE]

            if variable_cases:  # in case there is only permanent cases
                for i, leading_variable_case in enumerate(variable_cases):
                    # loop through every possible combination of leading + other variable for this unique combination
                    other_variable_cases = variable_cases[:i] + variable_cases[i+1:]

                    self.combinations.extend(generate_combination(c, permanent_cases, leading_variable_case, other_variable_cases, self.combination_type))

                    c += 1
            else:
                self.combinations.extend(
                    generate_combination(c, permanent_cases, None, [],
                                         self.combination_type))
                c += 1


if __name__ == "__main__":
    from desssign.loads.load_case import DesignLoadCase
    from desssign.loads.load_group import LoadGroup

    G1 = DesignLoadCase("G1", 'permanent')
    G2 = DesignLoadCase("G2", 'permanent')
    LG1 = LoadGroup([G1, G2], 'together')

    Q1 = DesignLoadCase("Q1", 'variable', 'category a')
    Q2 = DesignLoadCase("Q2", 'variable', 'category b')
    LG2 = LoadGroup([Q1, Q2], 'standard')

    S1 = DesignLoadCase("S1", 'variable', 'snow < 1000 m')
    S2 = DesignLoadCase("S2", 'variable', 'snow < 1000 m')
    S3 = DesignLoadCase("S3", 'variable', 'snow < 1000 m')
    LG3 = LoadGroup([S1, S2, S3], 'exclusive')

    W1 = DesignLoadCase("W1", 'variable', 'wind')
    W2 = DesignLoadCase("W2", 'variable', 'wind')
    W3 = DesignLoadCase("W3", 'variable', 'wind')
    W4 = DesignLoadCase("W4", 'variable', 'wind')
    LG4 = LoadGroup([W1, W2, W3, W4], 'exclusive')

    ULS = CombinationGroup('ULS', 'basic')

    ULS.generate_combinations(LG1, LG3, LG4)
    ULS.generate_combinations(LG1, LG2)

    print('')
