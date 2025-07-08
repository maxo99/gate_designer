"""
Material properties for structural steel grades
Following ASTM standards and engineering best practices
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict

@dataclass
class SteelProperties:
    """Steel material properties following ASTM standards"""
    grade: str
    yield_strength_Pa: float  # Minimum yield strength (Pa)
    ultimate_strength_Pa: float  # Minimum ultimate tensile strength (Pa)
    elastic_modulus_Pa: float  # Elastic modulus (Pa)
    density_kg_m3: float  # Density (kg/m³)
    poisson_ratio: float  # Poisson's ratio (dimensionless)
    thermal_expansion_per_C: float  # Thermal expansion coefficient (1/°C)
    
    @property
    def yield_strength_MPa(self) -> float:
        """Yield strength in MPa for convenience"""
        return self.yield_strength_Pa / 1e6
    
    @property
    def ultimate_strength_MPa(self) -> float:
        """Ultimate strength in MPa for convenience"""
        return self.ultimate_strength_Pa / 1e6
    
    @property
    def elastic_modulus_GPa(self) -> float:
        """Elastic modulus in GPa for convenience"""
        return self.elastic_modulus_Pa / 1e9

class SteelGrade(Enum):
    """Standard structural steel grades per ASTM specifications"""
    A36 = "A36"
    A572_50 = "A572_50"
    A588 = "A588"
    A992 = "A992"

# Steel properties database following ASTM standards
STEEL_PROPERTIES: Dict[SteelGrade, SteelProperties] = {
    SteelGrade.A36: SteelProperties(
        grade="ASTM A36",
        yield_strength_Pa=248e6,  # 36 ksi = 248 MPa (minimum)
        ultimate_strength_Pa=400e6,  # 58-80 ksi, using 58 ksi = 400 MPa (minimum)
        elastic_modulus_Pa=200e9,  # 200 GPa (29,000 ksi)
        density_kg_m3=7850,  # kg/m³
        poisson_ratio=0.30,
        thermal_expansion_per_C=12e-6  # 12 × 10⁻⁶ /°C
    ),
    
    SteelGrade.A572_50: SteelProperties(
        grade="ASTM A572 Grade 50",
        yield_strength_Pa=345e6,  # 50 ksi = 345 MPa (minimum)
        ultimate_strength_Pa=450e6,  # 65 ksi = 450 MPa (minimum)
        elastic_modulus_Pa=200e9,  # 200 GPa (29,000 ksi)
        density_kg_m3=7850,  # kg/m³
        poisson_ratio=0.30,
        thermal_expansion_per_C=12e-6  # 12 × 10⁻⁶ /°C
    ),
    
    SteelGrade.A588: SteelProperties(
        grade="ASTM A588 (Weathering Steel)",
        yield_strength_Pa=345e6,  # 50 ksi = 345 MPa (minimum)
        ultimate_strength_Pa=485e6,  # 70 ksi = 485 MPa (minimum)
        elastic_modulus_Pa=200e9,  # 200 GPa (29,000 ksi)
        density_kg_m3=7850,  # kg/m³
        poisson_ratio=0.30,
        thermal_expansion_per_C=12e-6  # 12 × 10⁻⁶ /°C
    ),
    
    SteelGrade.A992: SteelProperties(
        grade="ASTM A992 (Wide Flange)",
        yield_strength_Pa=345e6,  # 50 ksi = 345 MPa (minimum)
        ultimate_strength_Pa=450e6,  # 65 ksi = 450 MPa (minimum)
        elastic_modulus_Pa=200e9,  # 200 GPa (29,000 ksi)
        density_kg_m3=7850,  # kg/m³
        poisson_ratio=0.30,
        thermal_expansion_per_C=12e-6  # 12 × 10⁻⁶ /°C
    )
}

def get_material_properties(grade: SteelGrade) -> SteelProperties:
    """
    Get material properties for specified steel grade
    
    Args:
        grade: Steel grade enum
        
    Returns:
        SteelProperties object with all material properties
        
    Raises:
        ValueError: If steel grade is not supported
    """
    if grade not in STEEL_PROPERTIES:
        raise ValueError(f"Unsupported steel grade: {grade}")
    
    return STEEL_PROPERTIES[grade]

def get_material_properties_by_name(grade_name: str) -> SteelProperties:
    """
    Get material properties by grade name string
    
    Args:
        grade_name: Steel grade name (e.g., 'A572_50', 'A36')
        
    Returns:
        SteelProperties object
        
    Raises:
        ValueError: If steel grade name is not found
    """
    # Handle common naming variations
    grade_mapping = {
        'A36': SteelGrade.A36,
        'A572_50': SteelGrade.A572_50,
        'A572-50': SteelGrade.A572_50,
        'A572 Grade 50': SteelGrade.A572_50,
        'A588': SteelGrade.A588,
        'A992': SteelGrade.A992
    }
    
    if grade_name not in grade_mapping:
        available_grades = list(grade_mapping.keys())
        raise ValueError(f"Unknown steel grade: {grade_name}. Available grades: {available_grades}")
    
    return get_material_properties(grade_mapping[grade_name])

def validate_material_selection(grade: SteelGrade, application: str = "general") -> dict:
    """
    Validate material selection for specific application
    
    Args:
        grade: Steel grade to validate
        application: Application type ("general", "weathering", "high_strength")
        
    Returns:
        Dict with validation results and recommendations
    """
    props = get_material_properties(grade)
    warnings = []
    recommendations = []
    
    # Check yield strength adequacy
    if props.yield_strength_MPa < 250:
        warnings.append(f"Low yield strength ({props.yield_strength_MPa:.0f} MPa) - consider higher grade")
    
    # Application-specific checks
    if application == "weathering" and grade != SteelGrade.A588:
        recommendations.append("Consider A588 weathering steel for exposed applications")
    
    if application == "high_strength" and props.yield_strength_MPa < 345:
        recommendations.append("Consider A572 Grade 50 or higher for high-strength applications")
    
    # Ultimate to yield ratio check
    ult_yield_ratio = props.ultimate_strength_MPa / props.yield_strength_MPa
    if ult_yield_ratio < 1.2:
        warnings.append(f"Low ultimate/yield ratio ({ult_yield_ratio:.2f}) - check ductility requirements")
    
    return {
        "grade": props.grade,
        "yield_strength_MPa": f"{props.yield_strength_MPa:.0f}",
        "ultimate_strength_MPa": f"{props.ultimate_strength_MPa:.0f}",
        "warnings": warnings,
        "recommendations": recommendations,
        "status": "SUITABLE" if not warnings else "REVIEW_REQUIRED"
    }