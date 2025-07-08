"""
Material properties utility functions
Maintains compatibility with existing code while using updated core materials
"""

from src.core.materials import get_material_properties_by_name, SteelProperties
from typing import Dict, Any


def get_steel_properties(grade_name: str) -> SteelProperties:
    """
    Get steel properties by grade name

    Args:
        grade_name: Steel grade name (e.g., 'A572_50', 'A36')

    Returns:
        SteelProperties object with all material properties
    """
    return get_material_properties_by_name(grade_name)


def get_steel_properties_dict(grade_name: str) -> Dict[str, Any]:
    """
    Get steel properties as dictionary for backward compatibility

    Args:
        grade_name: Steel grade name

    Returns:
        Dictionary with material properties
    """
    props = get_steel_properties(grade_name)

    return {
        'grade': props.grade,
        'yield_strength_Pa': props.yield_strength_Pa,
        'ultimate_strength_Pa': props.ultimate_strength_Pa,
        'elastic_modulus_Pa': props.elastic_modulus_Pa,
        'density_kg_m3': props.density_kg_m3,
        'poisson_ratio': props.poisson_ratio,
        'thermal_expansion_per_C': props.thermal_expansion_per_C,
        'yield_strength_MPa': props.yield_strength_MPa,
        'ultimate_strength_MPa': props.ultimate_strength_MPa,
        'elastic_modulus_GPa': props.elastic_modulus_GPa
    }


# Common steel grades for quick reference
COMMON_GRADES = {
    'A36': 'General purpose structural steel',
    'A572_50': 'High-strength low-alloy steel (recommended for gates)',
    'A588': 'Weathering steel for outdoor applications',
    'A992': 'Wide flange beam steel'
}


def list_available_grades() -> Dict[str, str]:
    """Get list of available steel grades with descriptions"""
    return COMMON_GRADES.copy()
