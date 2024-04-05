import pytest
from unittest.mock import patch
from desssign.loads.snow.snow_load import calculate_shape_coefficient, calculate_snow_load_on_the_roof


def test_calculate_shape_coefficient() -> None:
    assert calculate_shape_coefficient(0, False) == 0.8
    assert calculate_shape_coefficient(30, False) == 0.8
    assert calculate_shape_coefficient(45, False) == 0.4
    assert calculate_shape_coefficient(60, False) == 0.0
    assert calculate_shape_coefficient(90, False) == 0.0
    assert calculate_shape_coefficient(0, True) == 0.8
    assert calculate_shape_coefficient(30, True) == 0.8
    assert calculate_shape_coefficient(45, True) == 0.8
    assert calculate_shape_coefficient(60, True) == 0.8


@patch('desssign.loads.snow.snow_load.EXPOSURE_COEFFICIENTS', {'topography1': 1.0})
@patch('desssign.loads.snow.snow_load.SNOW_LOAD_ON_THE_GROUND', {'snowzone1': 1.0})
def test_calculate_snow_load_on_the_roof() -> None:
    assert calculate_snow_load_on_the_roof(0, 'snowzone1', 'topography1', 1.0, False) == 0.8
    assert calculate_snow_load_on_the_roof(30, 'snowzone1', 'topography1', 1.0, False) == 0.8
    assert calculate_snow_load_on_the_roof(45, 'snowzone1', 'topography1', 1.0, False) == 0.4
    assert calculate_snow_load_on_the_roof(60, 'snowzone1', 'topography1', 1.0, False) == 0.0
    assert calculate_snow_load_on_the_roof(90, 'snowzone1', 'topography1', 1.0, False) == 0.0
    assert calculate_snow_load_on_the_roof(0, 'snowzone1', 'topography1', 1.0, True) == 0.8
    assert calculate_snow_load_on_the_roof(30, 'snowzone1', 'topography1', 1.0, True) == 0.8
    assert calculate_snow_load_on_the_roof(45, 'snowzone1', 'topography1', 1.0, True) == 0.8
    assert calculate_snow_load_on_the_roof(60, 'snowzone1', 'topography1', 1.0, True) == 0.8
