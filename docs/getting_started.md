# Getting Started with Cantilever Slide Gate Design Tool

## Overview

This tool helps you design cantilever slide gates based on proven reference designs (like the Tymetal Fortress) while customizing dimensions for your specific requirements.

## Quick Start

### 1. Run the Demo
```bash
uv run python demo.py
```

This will create a sample 6m x 2.4m gate design and show you the basic workflow.

### 2. Interactive Design
```bash
uv run python main.py
```

This will guide you through creating a custom gate design with your specific dimensions and requirements.

### 3. Review Results

After running either tool, check the `output/` directory for:
- **Calculation Summary** - Human-readable engineering results
- **Structural Calculations** - Detailed JSON data
- **Material List** - Bill of materials
- **Specifications** - Project specifications
- **Drawings** - Basic drawing information

## Design Process

### Step 1: Requirements Input
- Gate width and height (meters)
- Design wind speed (m/s)
- Steel grade (A36, A572_50, A992)
- Infill type (chain link, expanded metal, etc.)

### Step 2: Structural Analysis
The tool automatically:
- Calculates gate weight based on frame size and infill
- Determines wind loads per ASCE 7 standards
- Calculates overturning moments
- Sizes counterweight requirements
- Checks beam stresses and deflections

### Step 3: Design Optimization
- Reviews structural adequacy
- Provides design recommendations
- Flags potential issues

### Step 4: Documentation
- Generates calculation reports
- Creates material lists
- Produces specifications
- Provides installation notes

## Key Features

### Reference Integration
- Based on proven Tymetal Fortress design principles
- Maintains structural proportions while scaling
- Uses industry-standard connection details

### Engineering Standards
- Follows AISC steel design standards
- Applies ASCE 7 wind load calculations
- Uses appropriate safety factors (2.5 for structural)
- Metric units throughout (mm, N, Pa)

### Customization
- Scales reference design to your dimensions
- Selects appropriate steel grades
- Optimizes for local wind conditions
- Accommodates different infill types

## Understanding Results

### Key Calculations
- **Gate Weight**: Total weight of gate structure
- **Counterweight**: Required counterweight for stability
- **Wind Load**: Lateral force from design wind speed
- **Beam Stress**: Maximum stress in cantilever beam
- **Deflection**: Maximum deflection under load

### Design Adequacy
- **ADEQUATE**: Design meets all requirements
- **NEEDS REVISION**: Design requires modifications

### Design Notes
The tool provides specific recommendations:
- Stress limit warnings
- Deflection limit warnings
- Counterweight optimization suggestions
- Material selection recommendations

## Next Steps

### For Basic Users
1. Run the demo to understand the workflow
2. Use the interactive tool for your specific dimensions
3. Review the generated reports
4. Consult with a structural engineer for final approval

### For Engineers
1. Review calculation methods in `calculations/structural_analysis.py`
2. Customize material properties in `utils/material_properties.py`
3. Modify safety factors in `utils/engineering_constants.py`
4. Extend the reference design data in `reference/tymetal_fortress.py`

### For Developers
1. Study the modular architecture
2. Add new steel sections in `data/steel_sections.json`
3. Implement CAD integration in `designs/gate_designer.py`
4. Extend reporting capabilities in `documentation/report_generator.py`

## Safety and Disclaimers

⚠️ **Important**: This tool is for preliminary design and educational purposes. All designs must be reviewed and approved by a licensed structural engineer before construction.

- Results are based on simplified analysis methods
- Local building codes may have additional requirements
- Site-specific conditions may affect the design
- Professional engineering judgment is required for final approval

## Support and Resources

- **Reference Design**: Based on Tymetal Fortress specifications
- **Design Standards**: AISC Steel Construction Manual, ASCE 7
- **Code Repository**: All source code is available for review and modification
- **Documentation**: Complete calculation references included
