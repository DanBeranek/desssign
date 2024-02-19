from framesss.pre.cases import LoadCase

from desssign.loads.enums import LoadType, VariableCategory


class DesignLoadCase(LoadCase):
    def __init__(self, label: str, load_type: str | LoadType, category: str | VariableCategory = None) -> None:
        """Init the DesignLoadCase class."""
        super().__init__(label)
        self.load_type = LoadType(load_type)

        if self.load_type == LoadType.VARIABLE:
            self.category = VariableCategory(category)
        else:
            self.category = None

    def __repr__(self) -> str:
        """Return a string representation of the DesignLoadCase object."""
        # return (f"{self.__class__.__name__}("
        #         f"label={self.label}, "
        #         f"load_type={self.load_type}, "
        #         f"category={self.category})")
        return self.label


