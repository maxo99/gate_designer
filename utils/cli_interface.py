"""
Command line interface for gate design tool
"""

from designs.gate_designer import DesignRequirements


class CLIInterface:
    """Command line interface for user input"""
    
    def __init__(self):
        self.units = "metric"  # Default to metric units
    
    def get_design_requirements(self) -> DesignRequirements:
        """Get design requirements from user input"""
        
        print("Enter gate design requirements:")
        print("=" * 40)
        
        # Get basic dimensions
        width_m = self._get_float_input("Gate width (m)", default=6.0, min_val=3.0, max_val=20.0)
        height_m = self._get_float_input("Gate height (m)", default=2.4, min_val=1.5, max_val=5.0)
        
        # Convert to mm
        width_mm = width_m * 1000
        height_mm = height_m * 1000
        
        # Get design parameters
        wind_speed_ms = self._get_float_input("Design wind speed (m/s)", default=33.5, min_val=20.0, max_val=50.0)
        
        # Get material selection
        steel_grades = ['A36', 'A572_50', 'A992']
        print("\nAvailable steel grades:")
        for i, grade in enumerate(steel_grades, 1):
            print(f"{i}. {grade}")
        
        grade_choice = self._get_int_input("Select steel grade", default=2, min_val=1, max_val=len(steel_grades))
        steel_grade = steel_grades[grade_choice - 1]
        
        # Get infill type
        infill_types = ['chain_link', 'expanded_metal', 'solid_plate', 'custom']
        print("\nAvailable infill types:")
        for i, infill in enumerate(infill_types, 1):
            print(f"{i}. {infill.replace('_', ' ').title()}")
        
        infill_choice = self._get_int_input("Select infill type", default=1, min_val=1, max_val=len(infill_types))
        infill_type = infill_types[infill_choice - 1]
        
        # Create requirements object
        requirements = DesignRequirements(
            gate_width_mm=width_mm,
            gate_height_mm=height_mm,
            wind_speed_ms=wind_speed_ms,
            steel_grade=steel_grade,
            infill_type=infill_type
        )
        
        # Display summary
        print("\n" + "=" * 40)
        print("DESIGN REQUIREMENTS SUMMARY")
        print("=" * 40)
        print(f"Gate Size: {width_m:.1f}m x {height_m:.1f}m")
        print(f"Steel Grade: {steel_grade}")
        print(f"Infill Type: {infill_type.replace('_', ' ').title()}")
        print(f"Wind Speed: {wind_speed_ms:.1f} m/s")
        print()
        
        confirm = input("Proceed with design? (y/n): ").lower().strip()
        if confirm != 'y':
            print("Design cancelled.")
            exit()
        
        return requirements
    
    def _get_float_input(self, prompt: str, default: float, min_val: float | None = None, max_val: float | None = None) -> float:
        """Get float input with validation"""
        while True:
            try:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if not user_input:
                    value = default
                else:
                    value = float(user_input)
                
                if min_val is not None and value < min_val:
                    print(f"Value must be >= {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"Value must be <= {max_val}")
                    continue
                
                return value
                
            except ValueError:
                print("Please enter a valid number.")
    
    def _get_int_input(self, prompt: str, default: int, min_val: int | None = None, max_val: int | None = None) -> int:
        """Get integer input with validation"""
        while True:
            try:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if not user_input:
                    value = default
                else:
                    value = int(user_input)
                
                if min_val is not None and value < min_val:
                    print(f"Value must be >= {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"Value must be <= {max_val}")
                    continue
                
                return value
                
            except ValueError:
                print("Please enter a valid integer.")
    
    def display_results(self, design):
        """Display design results"""
        print("\n" + "=" * 50)
        print("DESIGN RESULTS")
        print("=" * 50)
        
        print(f"Gate Weight: {design.structural_results['gate_weight_kg']:.1f} kg")
        print(f"Counterweight: {design.structural_results['counterweight_kg']:.1f} kg")
        print(f"Maximum Stress: {design.structural_results['beam_stress_MPa']:.1f} MPa")
        print(f"Deflection: {design.structural_results['deflection_mm']:.1f} mm")
        
        if design.is_adequate:
            print("\n✓ Design is ADEQUATE")
        else:
            print("\n✗ Design NEEDS REVISION")
            for note in design.design_notes:
                print(f"  - {note}")
        
        print(f"\nOutput files saved to: {design.output_path}")
