"""
Core structural calculations for cantilever slide gates
"""

from typing import Dict
from dataclasses import dataclass

from utils.engineering_constants import GRAVITY_MS2
from utils.material_properties import SteelProperties


@dataclass
class LoadCase:
    """Represents a load case for structural analysis"""

    name: str
    dead_load_N: float
    live_load_N: float
    wind_load_N: float
    seismic_load_N: float = 0.0
    load_factor: float = 1.0


@dataclass
class GateGeometry:
    """Gate geometry parameters"""

    width_mm: float
    height_mm: float
    cantilever_length_mm: float
    track_length_mm: float
    counterweight_length_mm: float
    frame_depth_mm: float


class CantileverCalculations:
    """Structural calculations for cantilever slide gates"""

    def __init__(self, steel_properties: SteelProperties):
        self.steel = steel_properties
        self.safety_factor = 2.5  # Conservative safety factor

    def calculate_gate_weight(
        self,
        geometry: GateGeometry,
        frame_section_area_mm2: float,
        infill_weight_kg_m2: float = 25.0,
    ) -> float:
        """
        Calculate total gate weight in Newtons

        Args:
            geometry: Gate geometry parameters
            frame_section_area_mm2: Cross-sectional area of frame members
            infill_weight_kg_m2: Weight of infill material per m²

        Returns:
            Total gate weight in Newtons
        """
        # Frame weight calculation
        frame_perimeter_mm = 2 * (geometry.width_mm + geometry.height_mm)
        frame_volume_mm3 = frame_perimeter_mm * frame_section_area_mm2
        frame_weight_kg = frame_volume_mm3 * self.steel.density_kg_m3 / 1e9

        # Infill weight calculation
        infill_area_m2 = (geometry.width_mm * geometry.height_mm) / 1e6
        infill_weight_kg = infill_area_m2 * infill_weight_kg_m2

        # Total weight in Newtons
        total_weight_N = (frame_weight_kg + infill_weight_kg) * GRAVITY_MS2

        return total_weight_N

    def calculate_wind_load(
        self, geometry: GateGeometry, wind_speed_ms: float = 33.5
    ) -> float:
        """
        Calculate wind load on gate per ASCE 7

        Args:
            geometry: Gate geometry parameters
            wind_speed_ms: Design wind speed in m/s (default: 33.5 m/s = 75 mph)

        Returns:
            Wind load in Newtons
        """
        # Wind pressure calculation (ASCE 7-16)
        dynamic_pressure_Pa = 0.613 * wind_speed_ms**2

        # Drag coefficient for rectangular gate
        drag_coefficient = 1.2

        # Exposed area
        exposed_area_m2 = (geometry.width_mm * geometry.height_mm) / 1e6

        # Wind load
        wind_load_N = dynamic_pressure_Pa * drag_coefficient * exposed_area_m2

        return wind_load_N

    def calculate_cantilever_moment(
        self, geometry: GateGeometry, gate_weight_N: float, wind_load_N: float
    ) -> Dict[str, float]:
        """
        Calculate moments in cantilever beam

        Args:
            geometry: Gate geometry parameters
            gate_weight_N: Total gate weight
            wind_load_N: Wind load on gate

        Returns:
            Dictionary of moment values
        """
        # Moment arm for gate weight (to center of gravity)
        weight_moment_arm_mm = geometry.cantilever_length_mm / 2

        # Moment arm for wind load (to center of pressure)
        wind_moment_arm_mm = geometry.height_mm / 2

        # Dead load moment (overturning)
        dead_moment_Nmm = gate_weight_N * weight_moment_arm_mm

        # Wind moment (overturning)
        wind_moment_Nmm = wind_load_N * wind_moment_arm_mm

        # Total overturning moment
        total_overturning_Nmm = dead_moment_Nmm + wind_moment_Nmm

        return {
            "dead_moment_Nmm": dead_moment_Nmm,
            "wind_moment_Nmm": wind_moment_Nmm,
            "total_overturning_Nmm": total_overturning_Nmm,
        }

    def calculate_counterweight_requirement(
        self, geometry: GateGeometry, overturning_moment_Nmm: float
    ) -> float:
        """
        Calculate required counterweight

        Args:
            geometry: Gate geometry parameters
            overturning_moment_Nmm: Total overturning moment

        Returns:
            Required counterweight in Newtons
        """
        # Counterweight moment arm
        cw_moment_arm_mm = geometry.counterweight_length_mm

        # Required counterweight with safety factor
        required_cw_N = (overturning_moment_Nmm * self.safety_factor) / cw_moment_arm_mm

        return required_cw_N

    def calculate_track_loads(
        self,
        geometry: GateGeometry,
        gate_weight_N: float,
        counterweight_N: float,
    ) -> Dict[str, float]:
        """
        Calculate loads on track structure

        Args:
            geometry: Gate geometry parameters
            gate_weight_N: Total gate weight
            counterweight_N: Counterweight

        Returns:
            Dictionary of track load values
        """
        # Vertical loads
        front_wheel_load_N = gate_weight_N / 2  # Assuming 2 front wheels
        rear_wheel_load_N = (gate_weight_N / 2) + counterweight_N

        # Horizontal loads (from wind and friction)
        horizontal_load_N = gate_weight_N * 0.1  # 10% friction coefficient

        return {
            "front_wheel_load_N": front_wheel_load_N,
            "rear_wheel_load_N": rear_wheel_load_N,
            "horizontal_load_N": horizontal_load_N,
        }

    def calculate_beam_stress(
        self, moment_Nmm: float, section_modulus_mm3: float
    ) -> float:
        """
        Calculate bending stress in beam

        Args:
            moment_Nmm: Applied moment
            section_modulus_mm3: Section modulus of beam

        Returns:
            Bending stress in Pa
        """
        stress_Pa = moment_Nmm / section_modulus_mm3
        return stress_Pa

    def check_beam_adequacy(
        self, applied_stress_Pa: float, allowable_stress_Pa: float
    ) -> Dict[str, float]:
        """
        Check beam adequacy against allowable stress

        Args:
            applied_stress_Pa: Applied stress
            allowable_stress_Pa: Allowable stress

        Returns:
            Dictionary with adequacy check results
        """
        stress_ratio = applied_stress_Pa / allowable_stress_Pa
        is_adequate = stress_ratio <= 1.0

        return {
            "stress_ratio": stress_ratio,
            "is_adequate": is_adequate,
            "margin_percent": (1.0 - stress_ratio) * 100,
        }

    def calculate_deflection(
        self, load_N: float, length_mm: float, moment_of_inertia_mm4: float
    ) -> float:
        """
        Calculate beam deflection

        Args:
            load_N: Applied load
            length_mm: Beam length
            moment_of_inertia_mm4: Moment of inertia

        Returns:
            Deflection in mm
        """
        # For cantilever beam with end load
        deflection_mm = (load_N * length_mm**3) / (
            3 * self.steel.elastic_modulus_Pa * moment_of_inertia_mm4
        )

        return deflection_mm
