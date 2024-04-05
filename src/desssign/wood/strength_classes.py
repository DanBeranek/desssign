"""
The module contains mechanical properties of wood according to ČSN EN 338:2016.

E_m0mean: mean characteristic value of modulus of elasticity in bending parallel to grain (in kN/mm2)
E_t0,mean: mean characteristic value of modulus of elasticity in tension parallel to grain (in kN/mm2)
E_m0k: 5-percentile characteristic value of modulus of elasticity in bending parallel to grain (in kN/mm2)
E_t0k: 5-percentile characteristic value of modulus of elasticity in tension parallel to grain (in kN/mm2)
E_m90mean: mean characteristic value of modulus of elasticity in bending perpendicular to grain (in kN/mm2)
E_t90mean: mean characteristic value of modulus of elasticity in tension perpendicular to grain (in kN/mm2)
f_c0k: 5-percentile characteristic value of compressive strength parallel to grain (in N/mm2)
f_c90k: 5-percentile characteristic value of compressive strength perpendicular to grain (in N/mm2)
f_mk: 5-percentile characteristic value of bending strength (in N/mm2)
f_t0k: 5-percentile characteristic value of tensile strength parallel to grain (in N/mm2)
f_t90k: 5-percentile characteristic value of tensile strength perpendicular to grain (in N/mm2)
f_vk: 5-percentile characteristic value of shear strength (in N/mm2)
G_mean: mean characteristic value of shear modulus (in kN/mm2)
rho_k: 5-percentile characteristic value of density (in kg/m3)
rho_mean: mean characteristic value of density (in kg/m3)
"""

SOFTWOOD_STRENGTH_CLASSES = {
    "C14": {
        "f_mk": 14.0,
        "f_t0k": 7.2,
        "f_t90k": 0.4,
        "f_c0k": 16.0,
        "f_c90k": 2.0,
        "f_vk": 3.0,
        "E_m0mean": 7.0,
        "E_m0k": 4.7,
        "E_m90mean": 0.23,
        "G_mean": 0.44,
        "rho_k": 290.0,
        "rho_mean": 350.0,
    },
    "C16": {
        "f_mk": 16.0,
        "f_t0k": 8.5,
        "f_t90k": 0.4,
        "f_c0k": 17,
        "f_c90k": 2.2,
        "f_vk": 3.2,
        "E_m0mean": 8.0,
        "E_m0k": 5.4,
        "E_m90mean": 0.27,
        "G_mean": 0.5,
        "rho_k": 310.0,
        "rho_mean": 370.0,
    },
    "C18": {
        "f_mk": 18.0,
        "f_t0k": 10.0,
        "f_t90k": 0.4,
        "f_c0k": 18.0,
        "f_c90k": 2.2,
        "f_vk": 3.4,
        "E_m0mean": 9.0,
        "E_m0k": 6.0,
        "E_m90mean": 0.3,
        "G_mean": 0.56,
        "rho_k": 320.0,
        "rho_mean": 380.0,
    },
    "C20": {
        "f_mk": 20.0,
        "f_t0k": 11.5,
        "f_t90k": 0.4,
        "f_c0k": 19.0,
        "f_c90k": 2.3,
        "f_vk": 3.6,
        "E_m0mean": 9.5,
        "E_m0k": 6.4,
        "E_m90mean": 0.32,
        "G_mean": 0.59,
        "rho_k": 330.0,
        "rho_mean": 400.0,
    },
    "C22": {
        "f_mk": 22.0,
        "f_t0k": 13.0,
        "f_t90k": 0.4,
        "f_c0k": 20.0,
        "f_c90k": 2.4,
        "f_vk": 3.8,
        "E_m0mean": 10.0,
        "E_m0k": 6.7,
        "E_m90mean": 0.33,
        "G_mean": 0.63,
        "rho_k": 340.0,
        "rho_mean": 410.0,
    },
    "C24": {
        "f_mk": 24.0,
        "f_t0k": 14.5,
        "f_t90k": 0.4,
        "f_c0k": 21.0,
        "f_c90k": 2.5,
        "f_vk": 4.0,
        "E_m0mean": 11.0,
        "E_m0k": 7.4,
        "E_m90mean": 0.37,
        "G_mean": 0.69,
        "rho_k": 350.0,
        "rho_mean": 420.0,
    },
    "C27": {
        "f_mk": 27.0,
        "f_t0k": 16.5,
        "f_t90k": 0.4,
        "f_c0k": 22.0,
        "f_c90k": 2.5,
        "f_vk": 4.0,
        "E_m0mean": 11.5,
        "E_m0k": 7.7,
        "E_m90mean": 0.38,
        "G_mean": 0.72,
        "rho_k": 360.0,
        "rho_mean": 430.0,
    },
    "C30": {
        "f_mk": 30.0,
        "f_t0k": 19.0,
        "f_t90k": 0.4,
        "f_c0k": 24.0,
        "f_c90k": 2.7,
        "f_vk": 4.0,
        "E_m0mean": 12.0,
        "E_m0k": 8.0,
        "E_m90mean": 0.4,
        "G_mean": 0.75,
        "rho_k": 380.0,
        "rho_mean": 460.0,
    },
    "C35": {
        "f_mk": 35.0,
        "f_t0k": 22.5,
        "f_t90k": 0.4,
        "f_c0k": 25.0,
        "f_c90k": 2.7,
        "f_vk": 4.0,
        "E_m0mean": 13.0,
        "E_m0k": 8.7,
        "E_m90mean": 0.43,
        "G_mean": 0.81,
        "rho_k": 390.0,
        "rho_mean": 470.0,
    },
    "C40": {
        "f_mk": 40.0,
        "f_t0k": 26.0,
        "f_t90k": 0.4,
        "f_c0k": 27.0,
        "f_c90k": 2.8,
        "f_vk": 4.0,
        "E_m0mean": 14.0,
        "E_m0k": 9.4,
        "E_m90mean": 0.47,
        "G_mean": 0.88,
        "rho_k": 400.0,
        "rho_mean": 480.0,
    },
    "C45": {
        "f_mk": 45.0,
        "f_t0k": 30.0,
        "f_t90k": 0.4,
        "f_c0k": 29.0,
        "f_c90k": 2.9,
        "f_vk": 4.0,
        "E_m0mean": 15.0,
        "E_m0k": 10.1,
        "E_m90mean": 0.5,
        "G_mean": 0.94,
        "rho_k": 410.0,
        "rho_mean": 490.0,
    },
    "C50": {
        "f_mk": 50.0,
        "f_t0k": 33.5,
        "f_t90k": 0.4,
        "f_c0k": 30.0,
        "f_c90k": 3.0,
        "f_vk": 4.0,
        "E_m0mean": 16.0,
        "E_m0k": 10.7,
        "E_m90mean": 0.53,
        "G_mean": 1.0,
        "rho_k": 430.0,
        "rho_mean": 520.0,
    },
}


HARDWOOD_STRENGTH_CLASSES = {
    "D18": {
        "f_mk": 18.0,
        "f_t0k": 11.0,
        "f_t90k": 0.6,
        "f_c0k": 18.0,
        "f_c90k": 4.8,
        "f_vk": 3.5,
        "E_m0mean": 9.5,
        "E_m0k": 8.0,
        "E_m90mean": 0.63,
        "G_mean": 0.59,
        "rho_k": 475.0,
        "rho_mean": 570.0,
    },
    "D24": {
        "f_mk": 24.0,
        "f_t0k": 14.0,
        "f_t90k": 0.6,
        "f_c0k": 21.0,
        "f_c90k": 4.9,
        "f_vk": 3.7,
        "E_m0mean": 10.0,
        "E_m0k": 8.4,
        "E_m90mean": 0.67,
        "G_mean": 0.63,
        "rho_k": 485.0,
        "rho_mean": 580.0,
    },
    "D27": {
        "f_mk": 27.0,
        "f_t0k": 16.0,
        "f_t90k": 0.6,
        "f_c0k": 22.0,
        "f_c90k": 5.1,
        "f_vk": 3.8,
        "E_m0mean": 10.5,
        "E_m0k": 8.8,
        "E_m90mean": 0.7,
        "G_mean": 0.66,
        "rho_k": 510.0,
        "rho_mean": 610.0,
    },
    "D30": {
        "f_mk": 30.0,
        "f_t0k": 18.0,
        "f_t90k": 0.6,
        "f_c0k": 24.0,
        "f_c90k": 5.3,
        "f_vk": 3.9,
        "E_m0mean": 11.0,
        "E_m0k": 9.2,
        "E_m90mean": 0.73,
        "G_mean": 0.69,
        "rho_k": 530.0,
        "rho_mean": 640.0,
    },
    "D35": {
        "f_mk": 35.0,
        "f_t0k": 21.0,
        "f_t90k": 0.6,
        "f_c0k": 25.0,
        "f_c90k": 5.4,
        "f_vk": 4.1,
        "E_m0mean": 12.0,
        "E_m0k": 10.1,
        "E_m90mean": 0.8,
        "G_mean": 0.75,
        "rho_k": 540.0,
        "rho_mean": 650.0,
    },
    "D40": {
        "f_mk": 40.0,
        "f_t0k": 24.0,
        "f_t90k": 0.6,
        "f_c0k": 27.0,
        "f_c90k": 5.5,
        "f_vk": 4.2,
        "E_m0mean": 13.0,
        "E_m0k": 10.9,
        "E_m90mean": 0.87,
        "G_mean": 0.81,
        "rho_k": 550.0,
        "rho_mean": 660.0,
    },
    "D45": {
        "f_mk": 45.0,
        "f_t0k": 27.0,
        "f_t90k": 0.6,
        "f_c0k": 29.0,
        "f_c90k": 5.8,
        "f_vk": 4.4,
        "E_m0mean": 13.5,
        "E_m0k": 11.3,
        "E_m90mean": 0.9,
        "G_mean": 0.84,
        "rho_k": 580.0,
        "rho_mean": 700.0,
    },
    "D50": {
        "f_mk": 50.0,
        "f_t0k": 30.0,
        "f_t90k": 0.6,
        "f_c0k": 30.0,
        "f_c90k": 6.2,
        "f_vk": 4.5,
        "E_m0mean": 14.0,
        "E_m0k": 11.8,
        "E_m90mean": 0.93,
        "G_mean": 0.88,
        "rho_k": 620.0,
        "rho_mean": 740.0,
    },
    "D55": {
        "f_mk": 55.0,
        "f_t0k": 33.0,
        "f_t90k": 0.6,
        "f_c0k": 32.0,
        "f_c90k": 6.6,
        "f_vk": 4.7,
        "E_m0mean": 15.5,
        "E_m0k": 13.0,
        "E_m90mean": 1.03,
        "G_mean": 0.97,
        "rho_k": 660.0,
        "rho_mean": 790.0,
    },
    "D60": {
        "f_mk": 60.0,
        "f_t0k": 36.0,
        "f_t90k": 0.6,
        "f_c0k": 33.0,
        "f_c90k": 10.5,
        "f_vk": 4.8,
        "E_m0mean": 17.0,
        "E_m0k": 14.3,
        "E_m90mean": 1.13,
        "G_mean": 1.06,
        "rho_k": 700.0,
        "rho_mean": 840.0,
    },
    "D65": {
        "f_mk": 65.0,
        "f_t0k": 39.0,
        "f_t90k": 0.6,
        "f_c0k": 35.0,
        "f_c90k": 11.3,
        "f_vk": 5.0,
        "E_m0mean": 18.5,
        "E_m0k": 15.5,
        "E_m90mean": 1.23,
        "G_mean": 1.16,
        "rho_k": 750.0,
        "rho_mean": 900.0,
    },
    "D70": {
        "f_mk": 70.0,
        "f_t0k": 42.0,
        "f_t90k": 0.6,
        "f_c0k": 36.0,
        "f_c90k": 12.0,
        "f_vk": 5.0,
        "E_m0mean": 20.0,
        "E_m0k": 16.8,
        "E_m90mean": 1.33,
        "G_mean": 1.25,
        "rho_k": 800.0,
        "rho_mean": 960.0,
    },
    "D75": {
        "f_mk": 75.0,
        "f_t0k": 45.0,
        "f_t90k": 0.6,
        "f_c0k": 37.0,
        "f_c90k": 12.8,
        "f_vk": 5.0,
        "E_m0mean": 22.0,
        "E_m0k": 18.5,
        "E_m90mean": 1.47,
        "G_mean": 1.38,
        "rho_k": 850.0,
        "rho_mean": 1020.0,
    },
    "D80": {
        "f_mk": 80.0,
        "f_t0k": 48.0,
        "f_t90k": 0.6,
        "f_c0k": 38.0,
        "f_c90k": 13.5,
        "f_vk": 5.0,
        "E_m0mean": 24.0,
        "E_m0k": 20.2,
        "E_m90mean": 1.6,
        "G_mean": 1.5,
        "rho_k": 900.0,
        "rho_mean": 1080.0,
    },
}

WOOD_STRENGTH_CLASSES = {**SOFTWOOD_STRENGTH_CLASSES, **HARDWOOD_STRENGTH_CLASSES}
