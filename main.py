#!/usr/bin/env python3
"""
Cantilever Slide Gate Design Tool
Main application entry point

This tool helps design cantilever slide gates based on reference designs
and custom specifications.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from designs.gate_designer import CantileverGateDesigner
from utils.cli_interface import CLIInterface
from utils.config import load_config


def main():
    """Main application entry point"""
    print("=" * 60)
    print("CANTILEVER SLIDE GATE DESIGN TOOL")
    print("=" * 60)
    print()
    
    # Load configuration
    config = load_config()
    
    # Initialize CLI interface
    cli = CLIInterface()
    
    # Get user requirements
    requirements = cli.get_design_requirements()
    
    # Initialize gate designer
    designer = CantileverGateDesigner(config)
    
    # Create design
    try:
        gate_design = designer.create_design(requirements)
        
        # Generate outputs
        designer.generate_calculations(gate_design)
        designer.generate_drawings(gate_design)
        designer.generate_documentation(gate_design)
        
        print("\n" + "=" * 60)
        print("DESIGN COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Output files saved to: {gate_design.output_path}")
        print("\nGenerated files:")
        print("- Structural calculations")
        print("- Technical drawings")
        print("- Material specifications")
        print("- Assembly instructions")
        
    except Exception as e:
        print(f"\nError during design process: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
