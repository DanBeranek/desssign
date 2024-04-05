from desssign.loads.snow import snow_enums

EXPOSURE_COEFFICIENTS = {
    snow_enums.Topography.WINDSWEPT: 0.8,
    snow_enums.Topography.NORMAL: 1.0,
    snow_enums.Topography.SHELTERED: 1.2,
}

SNOW_LOAD_ON_THE_GROUND = {
    snow_enums.SnowZone.I: 0.7,
    snow_enums.SnowZone.II: 1.0,
    snow_enums.SnowZone.III: 1.5,
    snow_enums.SnowZone.IV: 2.0,
    snow_enums.SnowZone.V: 2.5,
    snow_enums.SnowZone.VI: 3.0,
    snow_enums.SnowZone.VII: 4.0,
    snow_enums.SnowZone.VIII: 0.0,
}
