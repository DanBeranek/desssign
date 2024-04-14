from numpy.testing import assert_almost_equal

from desssign.loads.wind.enums import FlatRoofType
from desssign.loads.wind.enums import TerrainCategory
from desssign.loads.wind.enums import WindZone
from desssign.loads.wind.roofs import FlatRoof


def test_flat_roof_with_sharp_eaves_low_building() -> None:
    """Case when 2 * h < b."""
    flat_roof = FlatRoof(
        roof_type=FlatRoofType.SHARP_EAVES,
        zone=WindZone.II,
        terrain_category=TerrainCategory.II,
        b_x=10.0,
        b_y=20.0,
        h=5.0,
    )

    # === ZONES GEOMETRY ===
    expected_geometry_x = [
        [[0.0, 0.0], [1.0, 0.0], [1.0, 2.5], [0.0, 2.5]],  # F
        [[0.0, 2.5], [1.0, 2.5], [1.0, 17.5], [0.0, 17.5]],  # G
        [[0.0, 17.5], [1.0, 17.5], [1.0, 20.0], [0.0, 20.0]],  # F
        [[1.0, 0.0], [5.0, 0.0], [5.0, 20.0], [1.0, 20.0]],  # H
        [[5.0, 0.0], [10.0, 0.0], [10.0, 20.0], [5.0, 20.0]],  # I
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [2.5, 0.0], [2.5, 1.0], [0.0, 1.0]],  # F
        [[2.5, 0.0], [7.5, 0.0], [7.5, 1.0], [2.5, 1.0]],  # G
        [[7.5, 0.0], [10.0, 0.0], [10.0, 1.0], [7.5, 1.0]],  # F
        [[0.0, 1.0], [10.0, 1.0], [10.0, 5.0], [0.0, 5.0]],  # H
        [[0.0, 5.0], [10.0, 5.0], [10.0, 20.0], [0.0, 20.0]],  # I
    ]

    zones_list = [
        flat_roof.zones_x_neg_pos or [],
        flat_roof.zones_x_neg_neg or [],
        flat_roof.zones_y_neg_pos or [],
        flat_roof.zones_y_neg_neg or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressures = [
        [-1.36, -0.90, -1.36, -0.53, +0.15],  # x pressure
        [-1.36, -0.90, -1.36, -0.53, -0.15],  # x suction
        [-1.36, -0.90, -1.36, -0.53, +0.15],  # y pressure
        [-1.36, -0.90, -1.36, -0.53, -0.15],  # y suction
    ]

    for zones, expected_values in zip(zones_list, expected_pressures):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)


def test_flat_roof_with_sharp_eaves_high_building() -> None:
    """Case when b < 2 * h."""
    flat_roof = FlatRoof(
        roof_type=FlatRoofType.SHARP_EAVES,
        zone=WindZone.II,
        terrain_category=TerrainCategory.II,
        b_x=10.0,
        b_y=20.0,
        h=30.0,
    )

    expected_geometry_x = [
        [[0.0, 0.0], [2.0, 0.0], [2.0, 5.0], [0.0, 5.0]],  # F
        [[0.0, 5.0], [2.0, 5.0], [2.0, 15.0], [0.0, 15.0]],  # G
        [[0.0, 15.0], [2.0, 15.0], [2.0, 20.0], [0.0, 20.0]],  # F
        [[2.0, 0.0], [10.0, 0.0], [10.0, 20.0], [2.0, 20.0]],  # H
        # There's no zone I, because the building is too high => H takes the rest of the space
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [2.5, 0.0], [2.5, 1.0], [0.0, 1.0]],  # F
        [[2.5, 0.0], [7.5, 0.0], [7.5, 1.0], [2.5, 1.0]],  # G
        [[7.5, 0.0], [10.0, 0.0], [10.0, 1.0], [7.5, 1.0]],  # F
        [[0.0, 1.0], [10.0, 1.0], [10.0, 5.0], [0.0, 5.0]],  # H
        [[0.0, 5.0], [10.0, 5.0], [10.0, 20.0], [0.0, 20.0]],  # I
    ]

    zones_list = [
        flat_roof.zones_x_neg_pos or [],
        flat_roof.zones_x_neg_neg or [],
        flat_roof.zones_y_neg_pos or [],
        flat_roof.zones_y_neg_neg or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressures = [
        [-2.18, -1.45, -2.18, -0.85],  # x pressure
        [-2.18, -1.45, -2.18, -0.85],  # x suction
        [-2.18, -1.45, -2.18, -0.85, +0.24],  # y pressure
        [-2.18, -1.45, -2.18, -0.85, -0.24],  # y suction
    ]

    for zones, expected_values in zip(zones_list, expected_pressures):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)


def test_flat_roof_with_parapets_low_building() -> None:
    flat_roof = FlatRoof(
        roof_type=FlatRoofType.WITH_PARAPETS,
        zone=WindZone.III,
        terrain_category=TerrainCategory.I,
        b_x=12.0,
        b_y=17.0,
        h=3.0,
        h_p=0.5,
    )

    # TODO: Check the newest EN 1991-1-4 (z_e = h + h_p), e = min(b, 2h)
    # === ZONES GEOMETRY ===
    expected_geometry_x = [
        [[0.0, 0.0], [0.6, 0.0], [0.6, 1.5], [0.0, 1.5]],  # F
        [[0.0, 1.5], [0.6, 1.5], [0.6, 15.5], [0.0, 15.5]],  # G
        [[0.0, 15.5], [0.6, 15.5], [0.6, 17.0], [0.0, 17.0]],  # F
        [[0.6, 0.0], [3.0, 0.0], [3.0, 17.0], [0.6, 17.0]],  # H
        [[3.0, 0.0], [12.0, 0.0], [12.0, 17.0], [3.0, 17.0]],  # I
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [1.5, 0.0], [1.5, 0.6], [0.0, 0.6]],  # F
        [[1.5, 0.0], [10.5, 0.0], [10.5, 0.6], [1.5, 0.6]],  # G
        [[10.5, 0.0], [12.0, 0.0], [12.0, 0.6], [10.5, 0.6]],  # F
        [[0.0, 0.6], [12.0, 0.6], [12.0, 3.0], [0.0, 3.0]],  # H
        [[0.0, 3.0], [12.0, 3.0], [12.0, 17.0], [0.0, 17.0]],  # I
    ]

    zones_list = [
        flat_roof.zones_x_neg_pos or [],
        flat_roof.zones_x_neg_neg or [],
        flat_roof.zones_y_neg_pos or [],
        flat_roof.zones_y_neg_neg or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressures = [
        [-1.23, -0.82, -1.23, -0.72, +0.21],  # x pressure
        [-1.23, -0.82, -1.23, -0.72, -0.21],  # x suction
        [-1.23, -0.82, -1.23, -0.72, +0.21],  # y pressure
        [-1.23, -0.82, -1.23, -0.72, -0.21],  # y suction
    ]

    for zones, expected_values in zip(zones_list, expected_pressures):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)


def test_flat_roof_with_parapets_high_building() -> None:
    flat_roof = FlatRoof(
        roof_type=FlatRoofType.WITH_PARAPETS,
        zone=WindZone.IV,
        terrain_category=TerrainCategory.III,
        b_x=10.0,
        b_y=5.0,
        h=14.0,
        h_p=0.5,
    )

    expected_geometry_x = [
        [[0.0, 0.0], [0.5, 0.0], [0.5, 1.25], [0.0, 1.25]],  # F
        [[0.0, 1.25], [0.5, 1.25], [0.5, 3.75], [0.0, 3.75]],  # G
        [[0.0, 3.75], [0.5, 3.75], [0.5, 5.0], [0.0, 5.0]],  # F
        [[0.5, 0.0], [2.5, 0.0], [2.5, 5.0], [0.5, 5.0]],  # H
        [[2.5, 0.0], [10.0, 0.0], [10.0, 5.0], [2.5, 5.0]],  # I
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [2.5, 0.0], [2.5, 1.0], [0.0, 1.0]],  # F
        [[2.5, 0.0], [7.5, 0.0], [7.5, 1.0], [2.5, 1.0]],  # G
        [[7.5, 0.0], [10.0, 0.0], [10.0, 1.0], [7.5, 1.0]],  # F
        [[0.0, 1.0], [10.0, 1.0], [10.0, 5.0], [0.0, 5.0]],  # H
        # There's no zone I, because the building is too high => H takes the rest of the space
    ]

    zones_list = [
        flat_roof.zones_x_neg_pos or [],
        flat_roof.zones_x_neg_neg or [],
        flat_roof.zones_y_neg_pos or [],
        flat_roof.zones_y_neg_neg or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressures = [
        [-1.67, -1.12, -1.67, -0.77, +0.22],  # x pressure
        [-1.67, -1.12, -1.67, -0.77, -0.22],  # x suction
        [-1.67, -1.12, -1.67, -0.77],  # y pressure
        [-1.67, -1.12, -1.67, -0.77],  # y suction
    ]

    for zones, expected_values in zip(zones_list, expected_pressures):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)
