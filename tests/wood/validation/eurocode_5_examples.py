"""
Test examples were taken from:
[1] KOŽELOUH, Bohumil. Příklady výpočtu podle Eurokódu 5 (I.). (2016),
    Available from: https://stavba.tzb-info.cz/drevene-konstrukce/13762-priklady-vypoctu-podle-eurokodu-5-i
[4] KOŽELOUH, Bohumil. Příklady výpočtu podle Eurokódu 5 (IV.). (2016),
    Available from: https://stavba.tzb-info.cz/drevene-konstrukce/13913-priklady-vypoctu-podle-eurokodu-5-iv
"""

import numpy as np
from numpy.testing import assert_almost_equal
from numpy.testing import assert_array_almost_equal

from framesss.solvers.linear_static import LinearStaticSolver

from desssign.wood.models import WoodModelFrameXZ
from desssign.loads.enums import LoadDurationClass
from desssign.wood.enums import ServiceClass
from desssign.wood.wood_section import WoodRectangularSection
from desssign.wood.wood_material import WoodMaterial


def test_example_1() -> None:
    """
    Example 1 from [1].
    The design flexural strength of a cross-section of softwood C24
    b/h = 100/140 mm for service class 2 and short-term loading is to be determined.
    """
    section = WoodRectangularSection(
        label="FOO",
        b=100.0,
        h=140.0,
        material=WoodMaterial(
            strength_class="C24",
            service_class=ServiceClass.SC2
        )
    )

    k_h = section.get_k_h('bending')

    f_md = k_h * section.material.get_design_value(
        characteristic_value=section.material.f_mk,
        load_duration_class=LoadDurationClass.SHORT_TERM
    )

    assert_almost_equal(f_md * 1E-6, 16.88, decimal=1)


def test_example_IV_1() -> None:
    """
    Example 1 from [4].
    """
    material = WoodMaterial("C24", ServiceClass.SC2)
    section = WoodRectangularSection("FOO", 0.1, 0.16, material)

    model = WoodModelFrameXZ()

    fixed = ["fixed", "free", "fixed", "free", "fixed", "free"]
    vertical_roller = ["fixed", "free", "free", "free", "free", "free"]

    node_1 = model.add_node("1", [0, 0, 0], fixity=fixed)
    node_2 = model.add_node("2", [6, 0, 0], fixity=fixed)
    node_3 = model.add_node("3", [12, 0, 0], fixity=fixed)
    node_4 = model.add_node("4", [3, 0, 4], fixity=vertical_roller)
    node_5 = model.add_node("5", [6, 0, 4])
    node_6 = model.add_node("6", [9, 0, 4], fixity=vertical_roller)

    member_14 = model.add_member("1-4", "navier", [node_1, node_4], section)
    member_45 = model.add_member(
        "4-5", "navier", [node_4, node_5], section, hinges=["fixed", "hinged"]
    )
    member_25 = model.add_member(
        "2-5", "navier", [node_2, node_5], section, hinges=["fixed", "hinged"]
    )
    member_56 = model.add_member(
        "5-6", "navier", [node_5, node_6], section, hinges=["hinged", "fixed"]
    )
    member_63 = model.add_member("6-3", "navier", [node_6, node_3], section)

    lc1 = model.add_load_case(
        "LC1",
        "variable",
        "a",
        "short-term"
    )
    node_1.add_prescribed_displacement(-0.003, "x", lc1)

    lc2 = model.add_load_case(
        "LC2",
        "permanent",
        load_duration_class="permanent"
    )
    node_3.add_prescribed_displacement(-0.003, "x", lc2)

    lc3 = model.add_load_case(
        "LC3",
        "variable",
        "wind",
        "instantaneous"
    )
    member_14.add_distributed_load(
        np.array([0, 0, 25, 0, 0, 25]) * 1E3, lc3, location="projection"
    )

    lc4 = model.add_load_case(
        "LC4",
        "permanent",
        load_duration_class="permanent"
    )
    member_45.add_distributed_load(np.array([0, 0, 25, 0, 0, 25]) * 1E3, lc4)

    lc5 = model.add_load_case(
        "LC5",
        "permanent",
        load_duration_class="permanent"
    )
    member_56.add_distributed_load(np.array([0, 0, -25, 0, 0, -25]) * 1E3, lc5)

    lc6 = model.add_load_case(
        "LC6",
        "permanent",
        load_duration_class="permanent"
    )
    member_63.add_distributed_load(
        np.array([0, 0, -25, 0, 0, -25]) * 1E3, lc6, location="projection"
    )

    comb = model.add_load_case_combination(
        label="CO1",
        limit_state="ULS",
        combination_type="basic",
        permanent_cases=[lc2, lc4, lc5, lc6],
        leading_variable_case=lc1,
        other_variable_cases=[lc3]
    )

    solver = LinearStaticSolver(model)
    solver.solve()

    model.perform_uls_checks()

    print("")
