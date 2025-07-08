#!/usr/bin/env python3
"""
Demo script for cantilever slide gate design tool
"""

from designs.gate_designer import CantileverGateDesigner, DesignRequirements
from utils.config import load_config


def run_demo():
    """Run a demonstration of the gate design tool"""
    
    print("=" * 60)
    print("CANTILEVER SLIDE GATE DESIGN TOOL - DEMO")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Create demo requirements
    requirements = DesignRequirements(
        gate_width_mm=6000,    # 6m wide gate
        gate_height_mm=2400,   # 2.4m high gate
        wind_speed_ms=33.5,    # 75 mph wind
        steel_grade='A572_50', # High strength steel
        infill_type='chain_link'
    )
    
    print("Demo Requirements:")
    print(f"- Gate Size: {requirements.gate_width_mm/1000:.1f}m x {requirements.gate_height_mm/1000:.1f}m")
    print(f"- Steel Grade: {requirements.steel_grade}")
    print(f"- Wind Speed: {requirements.wind_speed_ms:.1f} m/s")
    print(f"- Infill Type: {requirements.infill_type}")
    print()
    
    # Initialize designer
    designer = CantileverGateDesigner(config)
    
    # Create design
    try:
        print("Creating design...")
        gate_design = designer.create_design(requirements)
        
        print("Generating outputs...")
        designer.generate_calculations(gate_design)
        designer.generate_drawings(gate_design)
        designer.generate_documentation(gate_design)
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Display key results
        print("\nKEY RESULTS:")
        print(f"Gate Weight: {gate_design.structural_results['gate_weight_kg']:.1f} kg")
        print(f"Counterweight: {gate_design.structural_results['counterweight_kg']:.1f} kg")
        print(f"Wind Load: {gate_design.structural_results['wind_load_N']:.1f} N")
        print(f"Beam Stress: {gate_design.structural_results['beam_stress_MPa']:.1f} MPa")
        print(f"Deflection: {gate_design.structural_results['deflection_mm']:.1f} mm")
        
        print(f"\nDesign Status: {'ADEQUATE' if gate_design.is_adequate else 'NEEDS REVISION'}")
        
        if gate_design.design_notes:
            print("\nDesign Notes:")
            for note in gate_design.design_notes:
                print(f"  - {note}")
        
        print(f"\nOutput files saved to: {gate_design.output_path}")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_demo()
