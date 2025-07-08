"""
Reference design data from Tymetal Fortress cantilever slide gate
"""

from dataclasses import dataclass
from typing import Dict, List
from calculations.structural_analysis import GateGeometry


@dataclass
class TymetalFortressSpecs:
    """Specifications from Tymetal Fortress design"""
    model: str
    width_range_mm: tuple
    height_range_mm: tuple
    frame_section: str
    track_type: str
    counterweight_type: str
    features: List[str]


class TymetalFortressReference:
    """Reference design data from Tymetal Fortress gate"""
    
    def __init__(self):
        self.specifications = self._load_specifications()
        
    def _load_specifications(self) -> Dict[str, TymetalFortressSpecs]:
        """Load Tymetal Fortress specifications"""
        
        specs = {
            'fortress_12': TymetalFortressSpecs(
                model='Fortress 12',
                width_range_mm=(3600, 12000),  # 12' to 40'
                height_range_mm=(1800, 3600),  # 6' to 12'
                frame_section='HSS 6x6x1/4',
                track_type='Crane Rail 135lb',
                counterweight_type='Concrete Block',
                features=[
                    'Galvanized construction',
                    'Adjustable carrier wheels',
                    'Guide wheels',
                    'Weather seals',
                    'Manual override capability'
                ]
            ),
            'fortress_20': TymetalFortressSpecs(
                model='Fortress 20',
                width_range_mm=(6000, 20000),  # 20' to 65'
                height_range_mm=(1800, 4800),  # 6' to 16'
                frame_section='HSS 8x8x3/8',
                track_type='Crane Rail 175lb',
                counterweight_type='Steel Plate with Concrete',
                features=[
                    'Heavy-duty galvanized construction',
                    'Sealed bearing assemblies',
                    'Adjustable guide system',
                    'Weather protection',
                    'Emergency manual operation'
                ]
            )
        }
        
        return specs
    
    def get_reference_geometry(self, width_mm: float = 6000) -> GateGeometry:
        """Get reference geometry for scaling"""
        
        # Standard proportions from Tymetal design
        return GateGeometry(
            width_mm=width_mm,
            height_mm=width_mm * 0.4,  # 40% of width
            cantilever_length_mm=width_mm * 0.5,  # 50% of width
            track_length_mm=width_mm * 1.5,  # 150% of width
            counterweight_length_mm=width_mm * 0.3,  # 30% of width
            frame_depth_mm=200  # Standard frame depth
        )
    
    def get_frame_section_properties(self, gate_width_mm: float) -> Dict[str, str | float]:
        """Get frame section properties based on gate width"""
        
        if gate_width_mm <= 12000:
            # HSS 6x6x1/4 properties
            return {
                'section_name': 'HSS 6x6x1/4',
                'area_mm2': 5742,  # Cross-sectional area
                'moment_of_inertia_mm4': 42.7e6,  # Moment of inertia
                'section_modulus_mm3': 56.9e3,  # Section modulus
                'weight_kg_m': 45.1  # Weight per meter
            }
        else:
            # HSS 8x8x3/8 properties
            return {
                'section_name': 'HSS 8x8x3/8',
                'area_mm2': 8516,  # Cross-sectional area
                'moment_of_inertia_mm4': 105.8e6,  # Moment of inertia
                'section_modulus_mm3': 105.8e3,  # Section modulus
                'weight_kg_m': 66.9  # Weight per meter
            }
    
    def get_design_guidelines(self) -> Dict[str, str]:
        """Get design guidelines from Tymetal reference"""
        
        return {
            'cantilever_ratio': 'Cantilever length should be 40-60% of gate width',
            'counterweight_ratio': 'Counterweight should be 80-120% of gate weight',
            'track_length': 'Track length should be 120-150% of gate width',
            'foundation': 'Foundation should extend 150% of counterweight length',
            'clearances': 'Maintain 150mm minimum clearance around moving parts',
            'materials': 'Use hot-dip galvanized steel for corrosion protection',
            'connections': 'Use high-strength bolts for all structural connections',
            'maintenance': 'Provide access for lubrication and adjustment'
        }
    
    def get_installation_notes(self) -> List[str]:
        """Get installation notes from reference design"""
        
        return [
            'Foundation must be level and properly cured before installation',
            'Track rail must be aligned within 3mm over entire length',
            'Counterweight must be properly balanced and secured',
            'All connections must be torqued to specification',
            'Gate must be tested for smooth operation before final acceptance',
            'Lubrication points must be clearly marked and accessible',
            'Emergency stops must be clearly marked and functional'
        ]
