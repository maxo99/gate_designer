# Cantilever Slide Gate Design Tool

A comprehensive Python-based engineering design tool for creating custom cantilever slide gates based on proven reference designs.

## 🚀 Quick Start

### Run the Demo
```bash
uv run python demo.py
```

### Interactive Design
```bash
uv run python main.py
```

## 🏗️ Project Overview

This tool helps you design cantilever slide gates by:
- **Analyzing reference designs** (like the Tymetal Fortress gate)
- **Performing structural calculations** with proper safety factors
- **Customizing dimensions** for your specific requirements
- **Generating technical documentation** and material lists
- **Creating professional reports** for engineering review

## ✨ Features

### 🔧 Engineering Capabilities
- **Structural Analysis**: Load calculations, stress analysis, deflection checks
- **Wind Load Calculations**: ASCE 7 compliant wind load analysis
- **Material Optimization**: Steel grade selection and sizing
- **Safety Factors**: Industry-standard safety factors (2.5 for structural)
- **Code Compliance**: Follows AISC and ASCE standards

### 📊 Reference Integration
- **Tymetal Fortress Data**: Based on proven commercial gate designs
- **Proportional Scaling**: Maintains structural integrity while scaling
- **Industry Standards**: Uses standard connection details and practices

### 📋 Documentation
- **Calculation Reports**: Detailed engineering calculations
- **Material Lists**: Complete bill of materials
- **Specifications**: Professional project specifications
- **Installation Notes**: Construction and installation guidance

## 🏛️ Project Structure

```
├── main.py                 # Main application entry point
├── demo.py                 # Demonstration script
├── calculations/           # Structural engineering calculations
│   └── structural_analysis.py
├── designs/               # Gate design and optimization
│   └── gate_designer.py
├── documentation/         # Report generation
│   └── report_generator.py
├── reference/            # Reference designs and standards
│   └── tymetal_fortress.py
├── utils/               # Utility functions and constants
│   ├── cli_interface.py
│   ├── config.py
│   ├── engineering_constants.py
│   └── material_properties.py
├── data/                # Material properties and design data
│   └── steel_sections.json
├── output/              # Generated files and reports
└── docs/               # Documentation and guides
    └── getting_started.md
```

## 🔬 Technical Details

### Supported Steel Grades
- **A36**: Basic structural steel
- **A572 Grade 50**: High-strength steel (recommended)
- **A992**: Wide flange beam steel

### Design Parameters
- **Gate Width**: 3m to 20m
- **Gate Height**: 1.5m to 5m
- **Wind Speed**: Up to 50 m/s (112 mph)
- **Safety Factor**: 2.5 for structural elements

### Calculation Methods
- **Dead Load**: Based on material densities and geometry
- **Wind Load**: ASCE 7-16 wind pressure calculations
- **Moments**: Cantilever beam analysis
- **Stress Analysis**: Elastic beam theory
- **Deflection**: Standard beam deflection formulas

## 📈 Sample Results

For a 6m x 2.4m gate:
- **Gate Weight**: ~690 kg
- **Counterweight**: ~3,460 kg
- **Wind Load**: ~11,900 N (at 33.5 m/s)
- **Design Status**: Adequate with optimization notes

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- uv package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd cantilever-gate-design

# Install dependencies
uv sync

# Run demo
uv run python demo.py
```

## 🎯 Usage Examples

### Basic Design
```python
from designs.gate_designer import CantileverGateDesigner, DesignRequirements

requirements = DesignRequirements(
    gate_width_mm=6000,      # 6m wide
    gate_height_mm=2400,     # 2.4m high
    wind_speed_ms=33.5,      # 75 mph wind
    steel_grade='A572_50',   # High strength steel
    infill_type='chain_link'
)

designer = CantileverGateDesigner(config)
design = designer.create_design(requirements)
```

### Custom Analysis
```python
from calculations.structural_analysis import CantileverCalculations
from utils.material_properties import get_steel_properties

steel = get_steel_properties('A572_50')
calc = CantileverCalculations(steel)

# Perform specific calculations
gate_weight = calc.calculate_gate_weight(geometry, frame_area)
wind_load = calc.calculate_wind_load(geometry, wind_speed)
```

## 📚 Documentation

- **[Getting Started Guide](docs/getting_started.md)**: Complete setup and usage instructions
- **Code Documentation**: Inline documentation throughout the codebase
- **Reference Data**: Tymetal Fortress specifications and industry standards

## ⚠️ Safety and Disclaimers

**Important**: This tool is for preliminary design and educational purposes. All designs must be reviewed and approved by a licensed structural engineer before construction.

- Results are based on simplified analysis methods
- Local building codes may have additional requirements
- Site-specific conditions may affect the design
- Professional engineering judgment is required for final approval

## 🤝 Contributing

Contributions are welcome! Please:
1. Review the code structure and engineering standards
2. Follow the existing code style and documentation patterns
3. Add tests for new functionality
4. Update documentation for any changes

## 📄 License

This project is provided for educational and preliminary design purposes. Professional engineering review is required for any construction use.

## 🔗 References

- **Tymetal Fortress Gate**: https://www.tymetal.com/commercial-security-gates/cantilever-slide-gates/fortress-structural-cantilever-slide-gate/
- **AISC Steel Construction Manual**: American Institute of Steel Construction
- **ASCE 7**: Minimum Design Loads for Buildings and Other Structures
- **AWS D1.1**: Structural Welding Code
