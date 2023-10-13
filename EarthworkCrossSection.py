from __future__ import annotations
from dataclasses import dataclass
from math import floor


@dataclass
class EarthworkCrossSection:
    """
    Represents an earthwork cross section.

    Attributes:
        position (float): A station in feet.
        cut (float): Cut cross-sectional area in square feet.
        fill (float): Fill cross-sectional area in square feet.

    Private Attributes:
        _station (str): Position formatted as a station (##+##)

    """
    position: float = 0
    cut: float = 0
    fill: float = 0
    _station: str = None

    def __post_init__(self):
        """Generates station notation (##+##) from position."""
        if self._station is not None:
            # The station must have been set manually.
            return
        station_num = floor(self.position/100)
        station_addon = self.position - (station_num*100)
        self._station = f'{station_num}+{station_addon:02d}'

    def __repr__(self) -> str:
        return f'STA {self._station} ' + \
            f'cut: {self.cut:03.0f} sq ft & ' + \
            f'fill {self.fill:03.0f} sq ft'

    def find_distance_to(self, other: EarthworkCrossSection) -> float:
        """Finds the distance between this cross-section and another."""
        return abs(other.position - self.position)

    def find_cut_to(self, other: EarthworkCrossSection, swell: float = 0) -> float:
        """
        Computes the cut betwen this cross-section and another in cubic yards.
        Optional: specify a swell coefficient as a decimal (10% = 0.10), default 0
        """
        return (self.find_cutfill(
            self.find_distance_to(other),
            self.cut,
            other.cut
        ))*(1+swell)

    def find_fill_to(self, other: EarthworkCrossSection, shrink: float = 0) -> float:
        """
        Computes the fill betwen this cross-section and another in cubic yards.
        Optional: specify a shrink coefficient as a decimal (10% = 0.10), default 0.
        """
        return (self.find_cutfill(
            self.find_distance_to(other),
            self.fill,
            other.fill
        ))*(1+shrink)

    def find_earthwork_to(
            self,
            other: EarthworkCrossSection,
            shrink: float = 0,
            swell: float = 0) -> float:
        """
        Computes the total earthwork between this cross-section and 
        another, in cubic yards.
        The answer will represent how much earth must be removed.
        Optional: specify a shrink or swell oefficient as a 
        decimal (10% = 0.10), default 0
        """
        return (self.find_cut_to(other, swell) - self.find_fill_to(other, shrink))

    @staticmethod
    def find_cutfill(
            distance: float,
            cross_section_1: float,
            cross_section_2: float) -> float:
        """Computes the average volume along a distance and between two cross sections."""
        return distance * (cross_section_1 + cross_section_2) / (2*27)


def main() -> None:
    """ Demonstrates usage of EarthworkCrossSection objects to compute earthwork."""

    # First, use the EarthworkCrossSection class to build individual
    # cross-section objects:
    cross_section_1 = EarthworkCrossSection(position=1100, cut=350, fill=0)
    cross_section_2 = EarthworkCrossSection(position=1200, cut=150, fill=0)
    cross_section_3 = EarthworkCrossSection(position=1300, cut=0, fill=75)

    # Cross-section objects can be directly printed:
    print(cross_section_1)
    print(cross_section_2)
    print(cross_section_3)
    # Prints:
    # STA 11+00 cut: 350 sq ft & fill 000 sq ft
    # STA 12+00 cut: 150 sq ft & fill 000 sq ft
    # STA 13+00 cut: 000 sq ft & fill 075 sq ft

    # To calculate earthwork volume betwen adjacent sections, use
    # class functions (find_earthwork_to, find_cut_to, find_fill_to).
    # Shrink or swell can be specified manually (using keyword
    # arguments), but will default to 0% if excluded.
    earthwork_1_to_2 = cross_section_1.find_earthwork_to(cross_section_2,
                                                         swell=.3,
                                                         shrink=.1
                                                         )

    earthwork_2_to_3 = cross_section_2.find_earthwork_to(cross_section_3,
                                                         swell=.3,
                                                         shrink=.1
                                                         )

    total_earthwork_volume = earthwork_1_to_2 + earthwork_2_to_3
    print(f'{total_earthwork_volume:,.1f} cubic yards of earthwork needed.')
    # Prints: "1,412.0 cubic yards of earthwork needed."


if __name__ == '__main__':
    main()
