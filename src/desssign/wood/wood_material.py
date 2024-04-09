from __future__ import annotations

from framesss.pre.material import Material

from desssign.wood.strength_classes import WOOD_STRENGTH_CLASSES


class WoodMaterial(Material):
    """
    Class for structural wood material.

    Inherits from Material class and adds specific properties of wood.

    :param strength_class: Strength class of the wood material.
    """

    def __init__(self, strength_class: str) -> None:
        """Init the WoodMaterial object."""
        if strength_class not in WOOD_STRENGTH_CLASSES:
            raise ValueError(f"Invalid strength class: {strength_class}")

        self.strength_class = strength_class

        wood_properties = WOOD_STRENGTH_CLASSES[strength_class]

        self.f_mk = wood_properties["f_mk"]
        self.f_t0k = wood_properties["f_t0k"]
        self.f_t90k = wood_properties["f_t90k"]
        self.f_c0k = wood_properties["f_c0k"]
        self.f_c90k = wood_properties["f_c90k"]
        self.f_vk = wood_properties["f_vk"]
        self.E_m0mean = wood_properties["E_m0mean"]
        self.E_m0k = wood_properties["E_m0k"]
        self.E_m90mean = wood_properties["E_m90mean"]
        self.G_mean = wood_properties["G_mean"]
        self.rho_k = wood_properties["rho_k"]
        self.rho_mean = wood_properties["rho_mean"]

        poisson = self.E_m0k / (2 * self.G_mean) - 1

        super().__init__(
            label=strength_class,
            elastic_modulus=self.E_m0k,
            poissons_ratio=poisson,
            thermal_expansion_coefficient=0.5E-6,  # According to EN 1995-1-5, table C.1
            density=self.rho_mean,
        )

    def __repr__(self) -> str:
        """Return the string representation of the WoodMaterial object."""
        return f"WoodMaterial({self.strength_class})"
