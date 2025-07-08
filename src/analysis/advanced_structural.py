"""
Advanced structural analysis using engineering libraries
Updated to use proper material properties system
"""

import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from ..core.materials import SteelGrade, get_material_properties, get_material_properties_by_name


@dataclass
class BeamSection:
    """Structural beam section properties per AISC standards"""

    name: str
    depth_mm: float  # Overall depth
    width_mm: float  # Overall width
    thickness_mm: float  # Wall thickness
    area_mm2: float  # Cross-sectional area
    Ix_mm4: float  # Moment of inertia about x-axis (strong axis)
    Iy_mm4: float  # Moment of inertia about y-axis (weak axis)
    Sx_mm3: float  # Section modulus about x-axis
    Sy_mm3: float  # Section modulus about y-axis
    rx_mm: float   # Radius of gyration about x-axis
    ry_mm: float   # Radius of gyration about y-axis

    def __post_init__(self):
        """Validate section properties after initialization"""
        if self.area_mm2 <= 0:
            raise ValueError(f"Invalid cross-sectional area: {self.area_mm2} mm²")
        if self.Sx_mm3 <= 0:
            raise ValueError(f"Invalid section modulus: {self.Sx_mm3} mm³")
        if self.thickness_mm <= 0:
            raise ValueError(f"Invalid wall thickness: {self.thickness_mm} mm")


class AdvancedStructuralAnalyzer:
    """Advanced structural analysis using numerical methods per AISC 360"""

    def __init__(self, material_grade: str = 'A572_50'):
        """
        Initialize analyzer with material properties

        Args:
            material_grade: Steel grade name (e.g., 'A572_50', 'A36')
        """
        self.material = get_material_properties_by_name(material_grade)
        self.safety_factor = 2.5  # Per AISC recommendations for cantilever structures
        self.deflection_limit_ratio = 240  # L/240 per AISC

    def analyze_cantilever_beam(
        self,
        length_mm: float,
        distributed_load_N_per_mm: float,
        point_loads: List[Tuple[float, float]],
        section: BeamSection,
    ) -> Dict:
        """
        Comprehensive cantilever beam analysis per AISC 360

        Args:
            length_mm: Beam length in mm
            distributed_load_N_per_mm: Distributed load in N/mm
            point_loads: List of (position_mm, load_N) tuples
            section: Beam section properties

        Returns:
            Dict with complete analysis results including safety checks
        """

        # Input validation
        if length_mm <= 0:
            raise ValueError(f"Invalid beam length: {length_mm} mm")
        if distributed_load_N_per_mm < 0:
            raise ValueError(f"Invalid distributed load: {distributed_load_N_per_mm} N/mm")

        # Validate point loads
        for pos, load in point_loads:
            if pos < 0 or pos > length_mm:
                raise ValueError(f"Point load position {pos} mm outside beam length {length_mm} mm")
            if load < 0:
                raise ValueError(f"Invalid point load: {load} N (negative loads not supported)")

        # Create position array for analysis (1000 points for accuracy)
        x = np.linspace(0, length_mm, 1000)

        # Calculate internal forces and moments
        moments_Nmm = self._calculate_moment_distribution(
            x, length_mm, distributed_load_N_per_mm, point_loads
        )

        shears_N = self._calculate_shear_distribution(
            x, length_mm, distributed_load_N_per_mm, point_loads
        )

        # Calculate deflection using numerical integration
        deflections_mm = self._calculate_deflection_distribution(
            x, moments_Nmm, section.Ix_mm4
        )

        # Calculate maximum stresses per AISC 360
        max_moment_Nmm = np.max(np.abs(moments_Nmm))
        max_stress_Pa = max_moment_Nmm / section.Sx_mm3 * 1000  # Convert mm³ to m³

        # Safety checks per AISC 360
        allowable_stress_Pa = self.material.yield_strength_Pa / self.safety_factor
        stress_ratio = max_stress_Pa / allowable_stress_Pa

        # Deflection checks per AISC
        max_deflection_mm = np.max(np.abs(deflections_mm))
        deflection_limit_mm = length_mm / self.deflection_limit_ratio
        deflection_ratio = max_deflection_mm / deflection_limit_mm

        # Overall safety assessment
        safety_adequate = stress_ratio <= 1.0 and deflection_ratio <= 1.0

        # Calculate additional engineering parameters
        max_shear_N = np.max(np.abs(shears_N))

        return {
            'positions_mm': x,
            'moments_Nmm': moments_Nmm,
            'shears_N': shears_N,
            'deflections_mm': deflections_mm,
            'max_moment_Nmm': max_moment_Nmm,
            'max_stress_Pa': max_stress_Pa,
            'max_deflection_mm': max_deflection_mm,
            'max_shear_N': max_shear_N,
            'stress_ratio': stress_ratio,
            'deflection_ratio': deflection_ratio,
            'allowable_stress_Pa': allowable_stress_Pa,
            'deflection_limit_mm': deflection_limit_mm,
            'safety_adequate': safety_adequate,
            'material_grade': self.material.grade,
            'safety_factor': self.safety_factor,
            'yield_strength_Pa': self.material.yield_strength_Pa,
            'ultimate_strength_Pa': self.material.ultimate_strength_Pa,
            'elastic_modulus_Pa': self.material.elastic_modulus_Pa
        }

    def _calculate_moment_distribution(
        self,
        x: np.ndarray,
        length_mm: float,
        distributed_load_N_per_mm: float,
        point_loads: List[Tuple[float, float]],
    ) -> np.ndarray:
        """Calculate bending moment distribution for cantilever beam"""
        moments = np.zeros_like(x)

        for i, pos in enumerate(x):
            # Moment from distributed load (cantilever: M = wL²/2 at fixed end)
            if pos > 0:
                remaining_length = length_mm - pos
                distributed_moment = distributed_load_N_per_mm * remaining_length**2 / 2
                moments[i] += distributed_moment

            # Moment from point loads
            for load_pos, load_N in point_loads:
                if pos <= load_pos:  # Only consider loads beyond current position
                    moment_arm = load_pos - pos
                    moments[i] += load_N * moment_arm

        return moments

    def _calculate_shear_distribution(
        self,
        x: np.ndarray,
        length_mm: float,
        distributed_load_N_per_mm: float,
        point_loads: List[Tuple[float, float]],
    ) -> np.ndarray:
        """Calculate shear force distribution for cantilever beam"""
        shears = np.zeros_like(x)

        for i, pos in enumerate(x):
            # Shear from distributed load
            remaining_length = length_mm - pos
            distributed_shear = distributed_load_N_per_mm * remaining_length
            shears[i] += distributed_shear

            # Shear from point loads
            for load_pos, load_N in point_loads:
                if pos <= load_pos:  # Only consider loads beyond current position
                    shears[i] += load_N

        return shears

    def _calculate_deflection_distribution(
        self, x: np.ndarray, moments_Nmm: np.ndarray, Ix_mm4: float
    ) -> np.ndarray:
        """Calculate deflection using numerical integration of moment-curvature"""
        E_Pa = self.material.elastic_modulus_Pa

        # Convert units for calculation
        EI_Nm2 = E_Pa * Ix_mm4 * 1e-12  # Convert mm⁴ to m⁴

        # Calculate curvature (1/R = M/EI)
        curvature_per_m = moments_Nmm / (EI_Nm2 * 1e9)  # Convert back to 1/mm units

        # Double integration: curvature -> slope -> deflection
        dx = x[1] - x[0]  # Position increment

        # First integration: curvature to slope
        slope = np.zeros_like(x)
        for i in range(len(x) - 1, 0, -1):  # Integrate from free end to fixed end
            slope[i-1] = slope[i] + curvature_per_m[i] * dx

        # Second integration: slope to deflection
        deflection = np.zeros_like(x)
        for i in range(len(x) - 1, 0, -1):  # Integrate from free end to fixed end
            deflection[i-1] = deflection[i] + slope[i] * dx

        return deflection

    def optimize_beam_section(
        self, length_mm: float, loads: Dict, available_sections: List[BeamSection]
    ) -> BeamSection:
        """
        Optimize beam section selection using minimum weight approach

        Args:
            length_mm: Beam length
            loads: Load dictionary with distributed and point loads
            available_sections: List of available sections

        Returns:
            Optimal BeamSection that meets all requirements
        """
        suitable_sections = []

        # Check each section for adequacy
        for section in available_sections:
            try:
                # Quick analysis
                result = self.analyze_cantilever_beam(
                    length_mm=length_mm,
                    distributed_load_N_per_mm=loads.get('distributed_N_per_mm', 0),
                    point_loads=loads.get('point_loads', []),
                    section=section
                )

                if result['safety_adequate']:
                    weight_kg = section.area_mm2 * length_mm * self.material.density_kg_m3 / 1e9
                    suitable_sections.append((section, weight_kg, result))

            except Exception as e:
                print(f"Warning: Section {section.name} failed analysis: {e}")
                continue

        if not suitable_sections:
            raise ValueError("No suitable sections found for given loads")

        # Select minimum weight section
        optimal_section, min_weight, optimal_result = min(suitable_sections, key=lambda x: x[1])

        print(f"Optimal section selected: {optimal_section.name}")
        print(f"Weight: {min_weight:.1f} kg")
        print(f"Stress ratio: {optimal_result['stress_ratio']:.2f}")
        print(f"Deflection ratio: {optimal_result['deflection_ratio']:.2f}")

        return optimal_section

    def generate_load_combinations(
        self, dead_load_N_per_mm: float, live_load_N_per_mm: float, wind_load_N_per_mm: float
    ) -> Dict[str, float]:
        """
        Generate ASCE 7 load combinations for structural analysis

        Args:
            dead_load_N_per_mm: Dead load in N/mm
            live_load_N_per_mm: Live load in N/mm
            wind_load_N_per_mm: Wind load in N/mm

        Returns:
            Dictionary of load combinations per ASCE 7
        """
        combinations = {
            'Service': dead_load_N_per_mm + live_load_N_per_mm,
            'Dead + Wind': dead_load_N_per_mm + wind_load_N_per_mm,
            'LRFD_1': 1.4 * dead_load_N_per_mm,
            'LRFD_2': 1.2 * dead_load_N_per_mm + 1.6 * live_load_N_per_mm,
            'LRFD_3': 1.2 * dead_load_N_per_mm + 1.0 * live_load_N_per_mm + 1.0 * wind_load_N_per_mm,
            'LRFD_4': 1.2 * dead_load_N_per_mm + 1.6 * wind_load_N_per_mm,
            'LRFD_5': 0.9 * dead_load_N_per_mm + 1.6 * wind_load_N_per_mm
        }

        return combinations
