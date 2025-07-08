"""
Enhanced demonstration of the cantilever slide gate design system
Shows advanced engineering analysis, visualization, and reporting
"""
import os
from datetime import datetime

import numpy as np
from src.analysis.advanced_structural import AdvancedStructuralAnalyzer, BeamSection
from src.visualization.engineering_plots import EngineeringPlotter
from src.reports.excel_generator import ExcelReportGenerator
from src.core.materials import get_material_properties_by_name


def create_hss_section(name: str, depth_mm: float, width_mm: float, thickness_mm: float) -> BeamSection:
    """
    Create HSS (Hollow Structural Section) properties per AISC standards
    
    Args:
        name: Section designation (e.g., 'HSS150x150x6')
        depth_mm: Overall depth in mm
        width_mm: Overall width in mm
        thickness_mm: Wall thickness in mm
        
    Returns:
        BeamSection with calculated properties
    """
    # Input validation
    if depth_mm <= 0 or width_mm <= 0 or thickness_mm <= 0:
        raise ValueError(f"Invalid section dimensions: {depth_mm}x{width_mm}x{thickness_mm}")
    
    if thickness_mm >= min(depth_mm, width_mm) / 2:
        raise ValueError(f"Wall thickness {thickness_mm} mm too large for section {depth_mm}x{width_mm}")
    
    # Calculate section properties for rectangular HSS per AISC Steel Construction Manual
    outer_area_mm2 = depth_mm * width_mm
    inner_depth_mm = depth_mm - 2 * thickness_mm
    inner_width_mm = width_mm - 2 * thickness_mm
    inner_area_mm2 = inner_depth_mm * inner_width_mm
    
    # Net cross-sectional area
    area_mm2 = outer_area_mm2 - inner_area_mm2
    
    # Moment of inertia calculations (strong axis - about width)
    Ix_outer_mm4 = depth_mm * width_mm**3 / 12
    Ix_inner_mm4 = inner_depth_mm * inner_width_mm**3 / 12
    Ix_mm4 = Ix_outer_mm4 - Ix_inner_mm4
    
    # Moment of inertia (weak axis - about depth)
    Iy_outer_mm4 = width_mm * depth_mm**3 / 12
    Iy_inner_mm4 = inner_width_mm * inner_depth_mm**3 / 12
    Iy_mm4 = Iy_outer_mm4 - Iy_inner_mm4
    
    # Section modulus
    Sx_mm3 = Ix_mm4 / (width_mm / 2)
    Sy_mm3 = Iy_mm4 / (depth_mm / 2)
    
    # Radius of gyration
    rx_mm = np.sqrt(Ix_mm4 / area_mm2)
    ry_mm = np.sqrt(Iy_mm4 / area_mm2)
    
    return BeamSection(
        name=name,
        depth_mm=depth_mm,
        width_mm=width_mm,
        thickness_mm=thickness_mm,
        area_mm2=area_mm2,
        Ix_mm4=Ix_mm4,
        Iy_mm4=Iy_mm4,
        Sx_mm3=Sx_mm3,
        Sy_mm3=Sy_mm3,
        rx_mm=rx_mm,
        ry_mm=ry_mm
    )

def calculate_wind_load_per_ASCE7(wind_speed_ms: float, gate_height_mm: float, 
                                 exposure_category: str = 'C') -> float:
    """
    Calculate wind load per ASCE 7 standards
    
    Args:
        wind_speed_ms: Basic wind speed in m/s
        gate_height_mm: Gate height in mm
        exposure_category: Exposure category ('A', 'B', 'C', 'D')
        
    Returns:
        Wind pressure in Pa
    """
    # Convert wind speed to mph for ASCE 7 calculations
    wind_speed_mph = wind_speed_ms * 2.237
    
    # Basic wind pressure (ASCE 7-16 Equation 26.10-1)
    qz_Pa = 0.613 * (wind_speed_ms)**2  # Simplified for standard conditions
    
    # Gust factor (G = 0.85 for rigid structures)
    G = 0.85
    
    # Pressure coefficient (Cp = 1.2 for flat surfaces)
    Cp = 1.2
    
    # Wind pressure
    wind_pressure_Pa = qz_Pa * G * Cp
    
    return wind_pressure_Pa

def run_enhanced_demo():
    """Run comprehensive engineering demonstration with proper material properties"""
    print("🚀 Enhanced Cantilever Slide Gate Design System")
    print("=" * 60)
    
    # Gate configuration following engineering standards
    gate_config = {
        'project_name': 'Industrial Security Gate - Enhanced Analysis',
        'width_mm': 8000,  # 8m wide gate
        'height_mm': 2400,  # 2.4m high (standard)
        'wind_speed_ms': 45,  # 45 m/s wind speed (high wind region)
        'material_grade': 'A572_50',  # High-strength steel
        'safety_factor': 2.5,  # Conservative safety factor
        'gate_weight_kg': 1200,  # Estimated gate weight including infill
        'exposure_category': 'C'  # Open terrain exposure
    }
    
    print(f"📊 Analyzing {gate_config['width_mm']/1000:.1f}m × {gate_config['height_mm']/1000:.1f}m gate")
    print(f"🌪️  Design wind speed: {gate_config['wind_speed_ms']} m/s")
    print(f"🏗️  Material grade: {gate_config['material_grade']}")
    
    # Create multiple section options for comparison
    sections = [
        create_hss_section("HSS150x150x6", 150, 150, 6),
        create_hss_section("HSS200x200x8", 200, 200, 8),
        create_hss_section("HSS250x250x10", 250, 250, 10),
        create_hss_section("HSS300x300x12", 300, 300, 12)
    ]
    
    # Display section properties
    print("\n📐 Section Properties:")
    for section in sections:
        print(f"   {section.name}: Area = {section.area_mm2:.0f} mm², Sx = {section.Sx_mm3:.0f} mm³")
    
    # Initialize analyzer with material properties
    analyzer = AdvancedStructuralAnalyzer(material_grade=gate_config['material_grade'])
    
    # Display material properties
    material_props = analyzer.material
    print(f"\n🔬 Material Properties ({material_props.grade}):")
    print(f"   Yield Strength: {material_props.yield_strength_MPa:.0f} MPa")
    print(f"   Ultimate Strength: {material_props.ultimate_strength_MPa:.0f} MPa")
    print(f"   Elastic Modulus: {material_props.elastic_modulus_GPa:.0f} GPa")
    print(f"   Density: {material_props.density_kg_m3:.0f} kg/m³")
    
    # Calculate loads per engineering standards
    wind_pressure_Pa = calculate_wind_load_per_ASCE7(
        gate_config['wind_speed_ms'], 
        gate_config['height_mm'],
        gate_config['exposure_category']
    )
    
    # Load calculations
    distributed_wind_load_N_per_mm = wind_pressure_Pa * gate_config['height_mm'] / 1000  # N/mm
    distributed_dead_load_N_per_mm = (gate_config['gate_weight_kg'] * 9.81 / 
                                     gate_config['width_mm'])  # N/mm
    
    # Generate ASCE 7 load combinations
    load_combinations = analyzer.generate_load_combinations(
        dead_load_N_per_mm=distributed_dead_load_N_per_mm,
        live_load_N_per_mm=0,  # No live load for gates
        wind_load_N_per_mm=distributed_wind_load_N_per_mm
    )
    
    # Use governing load combination
    governing_load_N_per_mm = max(load_combinations.values())
    governing_combination = max(load_combinations, key=load_combinations.get)
    
    print(f"\n📈 Load Analysis:")
    print(f"   Wind pressure: {wind_pressure_Pa:.0f} Pa")
    print(f"   Distributed wind load: {distributed_wind_load_N_per_mm:.2f} N/mm")
    print(f"   Distributed dead load: {distributed_dead_load_N_per_mm:.2f} N/mm")
    print(f"   Governing combination: {governing_combination}")
    print(f"   Governing load: {governing_load_N_per_mm:.2f} N/mm")
    
    # Analyze each section
    analysis_results = []
    for i, section in enumerate(sections):
        print(f"\n🔧 Analyzing section {i+1}/{len(sections)}: {section.name}")
        
        # Point loads (hardware, operators, safety systems)
        point_loads = [
            (gate_config['width_mm'] * 0.8, 2000),  # Drive mechanism at 80% length
            (gate_config['width_mm'] * 0.9, 1000),  # Safety systems at 90% length
        ]
        
        try:
            # Perform detailed structural analysis
            result = analyzer.analyze_cantilever_beam(
                length_mm=gate_config['width_mm'],
                distributed_load_N_per_mm=governing_load_N_per_mm,
                point_loads=point_loads,
                section=section
            )
            
            # Add section info to results for reporting
            result['section'] = section
            result['section_modulus_mm3'] = section.Sx_mm3
            result['EI_Nm2'] = (analyzer.material.elastic_modulus_Pa * 
                               section.Ix_mm4 * 1e-12)
            
            analysis_results.append(result)
            
            # Print summary with engineering assessment
            status = "✅ ADEQUATE" if result['safety_adequate'] else "❌ INADEQUATE"
            print(f"   Max stress: {result['max_stress_Pa']/1e6:.1f} MPa "
                  f"(ratio: {result['stress_ratio']:.2f})")
            print(f"   Max deflection: {result['max_deflection_mm']:.1f} mm "
                  f"(ratio: {result['deflection_ratio']:.2f})")
            print(f"   Status: {status}")
            
            # Engineering warnings
            if result['stress_ratio'] > 0.8:
                print(f"   ⚠️  High stress utilization - consider larger section")
            if result['deflection_ratio'] > 0.8:
                print(f"   ⚠️  High deflection - may affect operation")
                
        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")
            continue
    
    # Create output directory with timestamp
    output_dir = f"output/enhanced_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate advanced visualizations
    print(f"\n📊 Generating advanced visualizations...")
    plotter = EngineeringPlotter()
    
    # Individual analysis reports for each adequate section
    for i, (section, result) in enumerate(zip(sections, analysis_results)):
        if result['safety_adequate']:
            report_path = os.path.join(output_dir, 
                                     f"structural_analysis_{section.name.replace('x', '_')}.png")
            plotter.create_structural_analysis_report(
                result, section, gate_config['width_mm'], report_path
            )
            print(f"   📈 Created analysis report: {report_path}")
    
    # Material comparison plot
    if analysis_results:
        comparison_path = os.path.join(output_dir, "material_comparison.png")
        plotter.create_material_optimization_plot(sections, analysis_results, comparison_path)
        print(f"   📊 Created comparison plot: {comparison_path}")
    
    # Generate comprehensive Excel reports
    print(f"\n📋 Generating comprehensive Excel reports...")
    excel_generator = ExcelReportGenerator()
    
    # Find optimal section (minimum weight that meets requirements)
    optimal_section = None
    optimal_result = None
    min_weight_kg = float('inf')
    
    for section, result in zip(sections, analysis_results):
        if result['safety_adequate']:
            weight_kg = (section.area_mm2 * gate_config['width_mm'] * 
                        material_props.density_kg_m3 / 1e9)
            if weight_kg < min_weight_kg:
                min_weight_kg = weight_kg
                optimal_section = section
                optimal_result = result
    
    if optimal_section:
        print(f"   🎯 Optimal section: {optimal_section.name}")
        print(f"   Weight: {min_weight_kg:.0f} kg")
        
        # Prepare material data for Excel report
        material_data = {
            'grade': material_props.grade,
            'yield_strength_Pa': material_props.yield_strength_Pa,
            'ultimate_strength_Pa': material_props.ultimate_strength_Pa,
            'elastic_modulus_Pa': material_props.elastic_modulus_Pa,
            'density_kg_m3': material_props.density_kg_m3,
            'poisson_ratio': material_props.poisson_ratio,
            'thermal_expansion_per_C': material_props.thermal_expansion_per_C,
            'section': {
                'name': optimal_section.name,
                'area_mm2': optimal_section.area_mm2,
                'Ix_mm4': optimal_section.Ix_mm4,
                'Iy_mm4': optimal_section.Iy_mm4,
                'Sx_mm3': optimal_section.Sx_mm3,
                'Sy_mm3': optimal_section.Sy_mm3,
                'rx_mm': optimal_section.rx_mm,
                'ry_mm': optimal_section.ry_mm
            }
        }
        
        excel_path = os.path.join(output_dir, "comprehensive_design_report.xlsx")
        excel_generator.create_comprehensive_report(
            gate_config, optimal_result, material_data, excel_path
        )
        print(f"   📊 Created Excel report: {excel_path}")
    else:
        print("   ⚠️  No adequate sections found - consider larger sections or reduced loads")
    
    # Generate engineering summary report
    summary_path = os.path.join(output_dir, "engineering_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("CANTILEVER SLIDE GATE DESIGN SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Project: {gate_config['project_name']}\n")
        f.write(f"Gate Size: {gate_config['width_mm']/1000:.1f}m × {gate_config['height_mm']/1000:.1f}m\n")
        f.write(f"Design Wind Speed: {gate_config['wind_speed_ms']} m/s\n")
        f.write(f"Material Grade: {material_props.grade}\n")
        f.write(f"Safety Factor: {gate_config['safety_factor']:.1f}\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("LOAD ANALYSIS:\n")
        f.write("-" * 15 + "\n")
        f.write(f"Wind Pressure: {wind_pressure_Pa:.0f} Pa\n")
        f.write(f"Governing Load Combination: {governing_combination}\n")
        f.write(f"Governing Load: {governing_load_N_per_mm:.2f} N/mm\n\n")
        
        f.write("SECTION COMPARISON:\n")
        f.write("-" * 20 + "\n")
        f.write("Section          | Weight (kg) | Stress Ratio | Deflection Ratio | Status\n")
        f.write("-" * 75 + "\n")
        
        for section, result in zip(sections, analysis_results):
            weight_kg = (section.area_mm2 * gate_config['width_mm'] * 
                        material_props.density_kg_m3 / 1e9)
            status = "ADEQUATE" if result['safety_adequate'] else "INADEQUATE"
            f.write(f"{section.name:15} | {weight_kg:10.0f} | {result['stress_ratio']:11.2f} | "
                   f"{result['deflection_ratio']:15.2f} | {status}\n")
        
        if optimal_section:
            f.write(f"\nRECOMMENDED SECTION: {optimal_section.name}\n")
            f.write(f"Total Weight: {min_weight_kg:.0f} kg\n")
            f.write(f"Max Stress: {optimal_result['max_stress_Pa']/1e6:.1f} MPa\n")
            f.write(f"Max Deflection: {optimal_result['max_deflection_mm']:.1f} mm\n")
            f.write(f"Stress Safety Margin: {(1/optimal_result['stress_ratio']-1)*100:.0f}%\n")
            f.write(f"Deflection Safety Margin: {(1/optimal_result['deflection_ratio']-1)*100:.0f}%\n")
    
    print(f"   📝 Created engineering summary: {summary_path}")
    
    # Final summary
    print(f"\n🎉 Enhanced Analysis Complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Generated {len([r for r in analysis_results if r['safety_adequate']])} structural analysis reports")
    print(f"📈 Created material comparison plots")
    print(f"📋 Generated comprehensive Excel documentation")
    
    if optimal_section:
        print(f"\n🎯 Engineering Recommendation:")
        print(f"   Section: {optimal_section.name}")
        print(f"   Weight: {min_weight_kg:.0f} kg")
        print(f"   Stress safety margin: {(1/optimal_result['stress_ratio']-1)*100:.0f}%")
        print(f"   Deflection safety margin: {(1/optimal_result['deflection_ratio']-1)*100:.0f}%")
        print(f"   Material utilization: {optimal_result['stress_ratio']*100:.0f}%")
    
    print(f"\n🔧 Engineering libraries utilized:")
    print(f"   • NumPy: Numerical computations and array operations")
    print(f"   • SciPy: Structural optimization and numerical integration")
    print(f"   • Matplotlib: Professional engineering plots and diagrams")
    print(f"   • Pandas: Data organization and analysis")
    print(f"   • OpenPyXL: Comprehensive Excel report generation")
    print(f"   • Seaborn: Statistical visualization enhancements")
    
    return output_dir, optimal_section, optimal_result

if __name__ == "__main__":
    run_enhanced_demo()