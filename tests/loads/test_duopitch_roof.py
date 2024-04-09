from numpy.testing import assert_almost_equal

from desssign.loads.wind.enums import TerrainCategory
from desssign.loads.wind.enums import WindZone
from desssign.loads.wind.roofs import DuopitchRoof


def test_duopitch_roof_10_degrees() -> None:
    roof = DuopitchRoof(
        zone=WindZone.IV,
        terrain_category=TerrainCategory.I,
        b_x=8.0,
        b_y=12.0,
        h=7.0,
        pitch_angle=10.0,
    )

    # === ZONES GEOMETRY ===
    expected_geometry_x = [
        [[0.0, 0.0], [1.2, 0.0], [1.2, 3.0], [0.0, 3.0]],  # F
        [[0.0, 3.0], [1.2, 3.0], [1.2, 9.0], [0.0, 9.0]],  # G
        [[0.0, 9.0], [1.2, 9.0], [1.2, 12.0], [0.0, 12.0]],  # F
        [[1.2, 0.0], [4.0, 0.0], [4.0, 12.0], [1.2, 12.0]],  # H
        [[4.0, 0.0], [5.2, 0.0], [5.2, 12.0], [4.0, 12.0]],  # J
        [[5.2, 0.0], [8.0, 0.0], [8.0, 12.0], [5.2, 12.0]],  # I
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [2.0, 0.0], [2.0, 0.8], [0.0, 0.8]],  # F
        [[2.0, 0.0], [4.0, 0.0], [4.0, 0.8], [2.0, 0.8]],  # G
        [[4.0, 0.0], [6.0, 0.0], [6.0, 0.8], [4.0, 0.8]],  # G
        [[6.0, 0.0], [8.0, 0.0], [8.0, 0.8], [6.0, 0.8]],  # F
        [[0.0, 0.8], [4.0, 0.8], [4.0, 4.0], [0.0, 4.0]],  # H
        [[4.0, 0.8], [8.0, 0.8], [8.0, 4.0], [4.0, 4.0]],  # H
        [[0.0, 4.0], [4.0, 4.0], [4.0, 12.0], [0.0, 12.0]],  # I
        [[4.0, 4.0], [8.0, 4.0], [8.0, 12.0], [4.0, 12.0]],  # I
    ]

    zones_list = [
        roof.zones_x_neg_neg or [],
        roof.zones_wind_x_neg_pos or [],
        roof.zones_wind_x_pos_neg or [],
        roof.zones_wind_x_pos_pos or [],
        roof.zones_wind_y or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressure = [
        [-1.88, -1.44, -1.88, -0.65, -1.15, -0.72],  # x: - / -
        [-1.88, -1.44, -1.88, -0.65, +0.15, +0.00],  # x: - / +
        [+0.14, +0.14, +0.14, +0.14, -1.15, -0.72],  # x: + / -
        [+0.14, +0.14, +0.14, +0.14, +0.15, +0.00],  # x: + / +
        [-2.09, -1.87, -1.87, -2.09, -0.94, -0.94, -0.79, -0.79],  # y: - / -
    ]

    for zones, expected_values in zip(zones_list, expected_pressure):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)


def test_duopitch_roof_43_degrees() -> None:
    roof = DuopitchRoof(
        zone=WindZone.I,
        terrain_category=TerrainCategory.III,
        b_x=10.0,
        b_y=10.0,
        h=13.5,
        pitch_angle=43.0,
    )

    # === ZONES GEOMETRY ===
    expected_geometry_x = [
        [[0.0, 0.0], [1.0, 0.0], [1.0, 2.5], [0.0, 2.5]],  # F
        [[0.0, 2.5], [1.0, 2.5], [1.0, 7.5], [0.0, 7.5]],  # G
        [[0.0, 7.5], [1.0, 7.5], [1.0, 10.0], [0.0, 10.0]],  # F
        [[1.0, 0.0], [5.0, 0.0], [5.0, 10.0], [1.0, 10.0]],  # H
        [[5.0, 0.0], [6.0, 0.0], [6.0, 10.0], [5.0, 10.0]],  # J
        [[6.0, 0.0], [10.0, 0.0], [10.0, 10.0], [6.0, 10.0]],  # I
    ]

    expected_geometry_y = [
        [[0.0, 0.0], [2.5, 0.0], [2.5, 1.0], [0.0, 1.0]],  # F
        [[2.5, 0.0], [5.0, 0.0], [5.0, 1.0], [2.5, 1.0]],  # G
        [[5.0, 0.0], [7.5, 0.0], [7.5, 1.0], [5.0, 1.0]],  # G
        [[7.5, 0.0], [10.0, 0.0], [10.0, 1.0], [7.5, 1.0]],  # F
        [[0.0, 1.0], [5.0, 1.0], [5.0, 5.0], [0.0, 5.0]],  # H
        [[5.0, 1.0], [10.0, 1.0], [10.0, 5.0], [5.0, 5.0]],  # H
        [[0.0, 5.0], [5.0, 5.0], [5.0, 10.0], [0.0, 10.0]],  # I
        [[5.0, 5.0], [10.0, 5.0], [10.0, 10.0], [5.0, 10.0]],  # I
    ]

    zones_list = [
        roof.zones_x_neg_neg or [],
        roof.zones_wind_x_neg_pos or [],
        roof.zones_wind_x_pos_neg or [],
        roof.zones_wind_x_pos_pos or [],
        roof.zones_wind_y or [],
    ]

    expected_geometry = [
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_x,
        expected_geometry_y,
    ]

    assert all(
        zones is not None for zones in zones_list
    )  # Zone lists should not contain None values.

    for zones, expected_values in zip(zones_list, expected_geometry):
        for zone, expected_geo in zip(zones, expected_values):
            assert zone.geometry == expected_geo

    # === WIND LOAD ===
    expected_pressure = [
        [-0.04, -0.04, -0.04, -0.02, -0.20, -0.14],  # x: - / -
        [-0.04, -0.04, -0.04, -0.02, +0.00, +0.00],  # x: - / +
        [+0.42, +0.42, +0.42, +0.35, -0.20, -0.14],  # x: + / -
        [+0.42, +0.42, +0.42, +0.35, +0.00, +0.00],  # x: + / +
        [-0.66, -0.85, -0.85, -0.66, -0.54, -0.54, -0.30, -0.30],  # y: - / -
    ]

    for zones, expected_values in zip(zones_list, expected_pressure):  # type: ignore[assignment]
        for zone, expected_value in zip(zones, expected_values):
            assert_almost_equal(zone.w_e, expected_value * 1000, decimal=-1)
