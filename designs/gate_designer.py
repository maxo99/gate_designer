"""
Main gate designer class for cantilever slide gates
"""

from typing import Dict, List
from dataclasses import dataclass, field
from pathlib import Path
import json

from calculations.structural_analysis import CantileverCalculations, GateGeometry
from utils.material_properties import get_steel_properties
from reference.tymetal_fortress import TymetalFortressReference
from documentation.report_generator import ReportGenerator


@dataclass
class DesignRequirements:
    """User requirements for gate design"""

    gate_width_mm: float
    gate_height_mm: float
    wind_speed_ms: float = 33.5  # Default 75 mph
    steel_grade: str = "A572_50"
    infill_type: str = "chain_link"
    load_requirements: Dict[str, float] = field(default_factory=dict)
    site_conditions: Dict[str, str] = field(default_factory=dict)


@dataclass
class GateDesign:
    """Complete gate design with all calculated parameters"""

    requirements: DesignRequirements
    geometry: GateGeometry
    structural_results: Dict[str, float]
    material_list: List[Dict[str, str | float | int]]
    output_path: Path
    is_adequate: bool = True
    design_notes: List[str] = field(default_factory=list)


class CantileverGateDesigner:
    """Main designer class for cantilever slide gates"""

    def __init__(self, config: Dict):
        self.config = config
        self.reference = TymetalFortressReference()
        self.report_generator = ReportGenerator()

    def create_design(self, requirements: DesignRequirements) -> GateDesign:
        """
        Create a complete gate design based on requirements

        Args:
            requirements: User design requirements

        Returns:
            Complete gate design
        """
        print(
            f"Creating design for {requirements.gate_width_mm / 1000:.1f}m x {requirements.gate_height_mm / 1000:.1f}m gate"
        )

        # Get material properties
        steel = get_steel_properties(requirements.steel_grade)

        # Initialize structural calculator
        calc = CantileverCalculations(steel)

        # Determine gate geometry based on requirements and reference design
        geometry = self._determine_geometry(requirements)

        # Perform structural calculations
        structural_results = self._perform_calculations(calc, geometry, requirements)

        # Check design adequacy
        is_adequate, design_notes = self._check_design_adequacy(structural_results)

        # Generate material list
        material_list = self._generate_material_list(geometry, steel)

        # Create output directory
        output_path = self._create_output_directory(requirements)

        # Create design object
        design = GateDesign(
            requirements=requirements,
            geometry=geometry,
            structural_results=structural_results,
            material_list=material_list,
            output_path=output_path,
            is_adequate=is_adequate,
            design_notes=design_notes,
        )

        return design

    def _determine_geometry(self, requirements: DesignRequirements) -> GateGeometry:
        """Determine gate geometry based on requirements"""

        # Apply scaling with engineering judgment based on requirements
        cantilever_length = requirements.gate_width_mm * 0.5  # 50% of width
        track_length = requirements.gate_width_mm * 1.5  # 150% of width
        counterweight_length = requirements.gate_width_mm * 0.3  # 30% of width
        frame_depth = min(
            200, requirements.gate_height_mm * 0.1
        )  # 10% of height, max 200mm

        geometry = GateGeometry(
            width_mm=requirements.gate_width_mm,
            height_mm=requirements.gate_height_mm,
            cantilever_length_mm=cantilever_length,
            track_length_mm=track_length,
            counterweight_length_mm=counterweight_length,
            frame_depth_mm=frame_depth,
        )

        return geometry

    def _perform_calculations(
        self,
        calc: CantileverCalculations,
        geometry: GateGeometry,
        requirements: DesignRequirements,
    ) -> Dict[str, float]:
        """Perform all structural calculations"""

        results = {}

        # Calculate gate weight
        frame_area_mm2 = 2500  # Assumed frame section area
        gate_weight_N = calc.calculate_gate_weight(geometry, frame_area_mm2)
        results["gate_weight_N"] = gate_weight_N
        results["gate_weight_kg"] = gate_weight_N / 9.81

        # Calculate wind load
        wind_load_N = calc.calculate_wind_load(geometry, requirements.wind_speed_ms)
        results["wind_load_N"] = wind_load_N

        # Calculate moments
        moments = calc.calculate_cantilever_moment(geometry, gate_weight_N, wind_load_N)
        results.update(moments)

        # Calculate required counterweight
        counterweight_N = calc.calculate_counterweight_requirement(
            geometry, moments["total_overturning_Nmm"]
        )
        results["counterweight_N"] = counterweight_N
        results["counterweight_kg"] = counterweight_N / 9.81

        # Calculate track loads
        track_loads = calc.calculate_track_loads(
            geometry, gate_weight_N, counterweight_N
        )
        results.update(track_loads)

        # Calculate beam stresses (simplified)
        section_modulus_mm3 = 1e6  # Assumed section modulus
        beam_stress_Pa = calc.calculate_beam_stress(
            moments["total_overturning_Nmm"], section_modulus_mm3
        )
        results["beam_stress_Pa"] = beam_stress_Pa
        results["beam_stress_MPa"] = beam_stress_Pa / 1e6

        # Calculate deflection
        moment_of_inertia_mm4 = 1e8  # Assumed moment of inertia
        deflection_mm = calc.calculate_deflection(
            gate_weight_N, geometry.cantilever_length_mm, moment_of_inertia_mm4
        )
        results["deflection_mm"] = deflection_mm

        return results

    def _check_design_adequacy(self, results: Dict[str, float]) -> tuple:
        """Check if design is adequate"""

        is_adequate = True
        notes = []

        # Check stress limits
        if results["beam_stress_MPa"] > 200:  # Simplified check
            is_adequate = False
            notes.append("Beam stress exceeds allowable limits")

        # Check deflection limits
        if results["deflection_mm"] > 50:  # L/240 limit
            is_adequate = False
            notes.append("Deflection exceeds allowable limits")

        # Check counterweight reasonableness
        if results["counterweight_kg"] > results["gate_weight_kg"] * 2:
            notes.append("Counterweight is very heavy - consider design optimization")

        return is_adequate, notes

    def _generate_material_list(self, geometry: GateGeometry, steel) -> List[Dict]:
        """Generate material list for the gate"""

        materials = []

        # Main frame members
        materials.append(
            {
                "item": "Main Frame HSS",
                "size": "150x150x6",
                "length_mm": 2 * (geometry.width_mm + geometry.height_mm),
                "weight_kg": 150,  # Estimated
                "material": steel.grade,
            }
        )

        # Track rail
        materials.append(
            {
                "item": "Track Rail",
                "size": "CR135",
                "length_mm": geometry.track_length_mm,
                "weight_kg": 135 * geometry.track_length_mm / 1000,
                "material": steel.grade,
            }
        )

        # Counterweight
        materials.append(
            {
                "item": "Counterweight",
                "size": "Concrete Block",
                "weight_kg": geometry.counterweight_length_mm * 0.5,  # Estimated
                "material": "Concrete",
            }
        )

        return materials

    def _create_output_directory(self, requirements: DesignRequirements) -> Path:
        """Create output directory for design files"""

        output_dir = (
            Path("output")
            / f"gate_{requirements.gate_width_mm / 1000:.1f}x{requirements.gate_height_mm / 1000:.1f}m"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir

    def generate_calculations(self, design: GateDesign):
        """Generate calculation report"""
        calc_file = design.output_path / "structural_calculations.json"

        with open(calc_file, "w") as f:
            json.dump(design.structural_results, f, indent=2)

        print(f"Calculations saved to: {calc_file}")

    def generate_drawings(self, design: GateDesign):
        """Generate technical drawings"""
        # This would integrate with CAD tools
        drawing_file = design.output_path / "gate_drawings.txt"

        with open(drawing_file, "w") as f:
            f.write("CANTILEVER SLIDE GATE DRAWINGS\n")
            f.write("=" * 40 + "\n\n")
            f.write(
                f"Gate Dimensions: {design.geometry.width_mm / 1000:.1f}m x {design.geometry.height_mm / 1000:.1f}m\n"
            )
            f.write(
                f"Cantilever Length: {design.geometry.cantilever_length_mm / 1000:.1f}m\n"
            )
            f.write(f"Track Length: {design.geometry.track_length_mm / 1000:.1f}m\n")
            f.write(
                f"Counterweight Length: {design.geometry.counterweight_length_mm / 1000:.1f}m\n"
            )

        print(f"Drawings saved to: {drawing_file}")

    def generate_documentation(self, design: GateDesign):
        """Generate project documentation"""
        self.report_generator.generate_full_report(design)
