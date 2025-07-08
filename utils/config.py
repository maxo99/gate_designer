"""
Configuration management for gate design tool
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from file or create default"""
    
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # Create default configuration
        default_config = {
            "units": "metric",
            "safety_factors": {
                "structural": 2.5,
                "foundation": 3.0,
                "fatigue": 2.0
            },
            "default_materials": {
                "steel_grade": "A572_50",
                "infill_type": "chain_link"
            },
            "design_parameters": {
                "wind_speed_ms": 33.5,
                "seismic_zone": "low",
                "exposure_category": "C"
            },
            "output_settings": {
                "generate_drawings": True,
                "generate_calculations": True,
                "generate_specifications": True
            }
        }
        
        # Save default configuration
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config


def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    
    config_file = Path("config.json")
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
