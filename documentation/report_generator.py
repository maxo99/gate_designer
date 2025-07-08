"""
Report generator for cantilever slide gate documentation
"""

from pathlib import Path
import json
from datetime import datetime


class ReportGenerator:
    """Generate professional reports for gate designs"""
    
    def __init__(self):
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
    
    def generate_full_report(self, design):
        """Generate complete design report"""
        
        # Generate calculation summary
        self._generate_calculation_summary(design)
        
        # Generate material list
        self._generate_material_list(design)
        
        # Generate specifications
        self._generate_specifications(design)
        
        print(f"Complete documentation generated in: {design.output_path}")
    
    def _generate_calculation_summary(self, design):
        """Generate calculation summary report"""
        
        report_file = design.output_path / "calculation_summary.txt"
        
        with open(report_file, 'w') as f:
            f.write("CANTILEVER SLIDE GATE CALCULATION SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Project Date: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"Gate Size: {design.geometry.width_mm/1000:.1f}m x {design.geometry.height_mm/1000:.1f}m\n")
            f.write(f"Steel Grade: {design.requirements.steel_grade}\n")
            f.write(f"Design Wind Speed: {design.requirements.wind_speed_ms:.1f} m/s\n\n")
            
            f.write("STRUCTURAL RESULTS:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Gate Weight: {design.structural_results['gate_weight_kg']:.1f} kg\n")
            f.write(f"Counterweight: {design.structural_results['counterweight_kg']:.1f} kg\n")
            f.write(f"Wind Load: {design.structural_results['wind_load_N']:.1f} N\n")
            f.write(f"Beam Stress: {design.structural_results['beam_stress_MPa']:.1f} MPa\n")
            f.write(f"Deflection: {design.structural_results['deflection_mm']:.1f} mm\n\n")
            
            f.write("DESIGN ADEQUACY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Design Status: {'ADEQUATE' if design.is_adequate else 'NEEDS REVISION'}\n")
            if design.design_notes:
                f.write("Design Notes:\n")
                for note in design.design_notes:
                    f.write(f"  - {note}\n")
    
    def _generate_material_list(self, design):
        """Generate detailed material list"""
        
        material_file = design.output_path / "material_list.json"
        
        with open(material_file, 'w') as f:
            json.dump(design.material_list, f, indent=2)
    
    def _generate_specifications(self, design):
        """Generate project specifications"""
        
        spec_file = design.output_path / "specifications.txt"
        
        with open(spec_file, 'w') as f:
            f.write("CANTILEVER SLIDE GATE SPECIFICATIONS\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("GENERAL REQUIREMENTS:\n")
            f.write("- Gate shall be cantilever slide type\n")
            f.write("- All steel shall be hot-dip galvanized\n")
            f.write("- Gate shall operate smoothly with minimal force\n")
            f.write("- Design shall comply with local building codes\n\n")
            
            f.write("MATERIALS:\n")
            f.write(f"- Steel Grade: {design.requirements.steel_grade}\n")
            f.write(f"- Infill Type: {design.requirements.infill_type}\n")
            f.write("- Hardware: Stainless steel where exposed\n")
            f.write("- Finish: Hot-dip galvanized per ASTM A123\n\n")
            
            f.write("PERFORMANCE REQUIREMENTS:\n")
            f.write(f"- Wind Load: {design.requirements.wind_speed_ms:.1f} m/s\n")
            f.write("- Operating Temperature: -40°C to +60°C\n")
            f.write("- Service Life: 25 years minimum\n")
            f.write("- Maintenance: Annual inspection required\n")
