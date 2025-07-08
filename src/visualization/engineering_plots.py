"""
Advanced engineering visualization using matplotlib
"""

from typing import Dict, List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from src.analysis.advanced_structural import BeamSection


class EngineeringPlotter:
    """Create professional engineering plots and diagrams"""

    def __init__(self, style: str = "seaborn-v0_8-whitegrid"):
        plt.style.use(style)
        self.fig_size = (12, 8)
        self.dpi = 300

    def create_structural_analysis_report(
        self,
        analysis_results: Dict,
        section: BeamSection,
        gate_width_mm: float,
        output_path: str,
    ) -> None:
        """Create comprehensive structural analysis report with plots"""

        # Create multi-panel figure
        fig = plt.figure(figsize=(16, 12), dpi=self.dpi)
        gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

        # Plot 1: Moment Diagram
        ax1 = fig.add_subplot(gs[0, :])
        self._plot_moment_diagram(ax1, analysis_results)

        # Plot 2: Shear Diagram
        ax2 = fig.add_subplot(gs[1, 0])
        self._plot_shear_diagram(ax2, analysis_results)

        # Plot 3: Deflection Diagram
        ax3 = fig.add_subplot(gs[1, 1])
        self._plot_deflection_diagram(ax3, analysis_results)

        # Plot 4: Gate Elevation View
        ax4 = fig.add_subplot(gs[2, :])
        self._plot_gate_elevation(ax4, gate_width_mm, section)

        # Add title and summary
        fig.suptitle(
            "Cantilever Slide Gate - Structural Analysis Report",
            fontsize=16,
            fontweight="bold",
        )

        # Add summary text box
        summary_text = self._create_summary_text(analysis_results, section)
        fig.text(
            0.02,
            0.98,
            summary_text,
            transform=fig.transFigure,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close()

    def _plot_moment_diagram(self, ax, results: Dict) -> None:
        """Plot bending moment diagram"""
        x_m = results["positions_mm"] / 1000  # Convert to meters
        moments_kNm = results["moments_Nmm"] / 1e6  # Convert to kN⋅m

        ax.plot(x_m, moments_kNm, "b-", linewidth=2, label="Bending Moment")
        ax.fill_between(x_m, 0, moments_kNm, alpha=0.3, color="blue")

        # Mark maximum moment
        max_idx = np.argmax(np.abs(moments_kNm))
        ax.plot(x_m[max_idx], moments_kNm[max_idx], "ro", markersize=8)
        ax.annotate(
            f"Max: {moments_kNm[max_idx]:.1f} kN⋅m",
            xy=(x_m[max_idx], moments_kNm[max_idx]),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        )

        ax.set_xlabel("Position (m)")
        ax.set_ylabel("Bending Moment (kN⋅m)")
        ax.set_title("Bending Moment Diagram")
        ax.grid(True, alpha=0.3)
        ax.legend()

    def _plot_shear_diagram(self, ax, results: Dict) -> None:
        """Plot shear force diagram"""
        x_m = results["positions_mm"] / 1000
        shears_kN = results["shears_N"] / 1000

        ax.plot(x_m, shears_kN, "g-", linewidth=2, label="Shear Force")
        ax.fill_between(x_m, 0, shears_kN, alpha=0.3, color="green")

        # Mark maximum shear
        max_idx = np.argmax(np.abs(shears_kN))
        ax.plot(x_m[max_idx], shears_kN[max_idx], "ro", markersize=8)
        ax.annotate(
            f"Max: {shears_kN[max_idx]:.1f} kN",
            xy=(x_m[max_idx], shears_kN[max_idx]),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        )

        ax.set_xlabel("Position (m)")
        ax.set_ylabel("Shear Force (kN)")
        ax.set_title("Shear Force Diagram")
        ax.grid(True, alpha=0.3)
        ax.legend()

    def _plot_deflection_diagram(self, ax, results: Dict) -> None:
        """Plot deflection diagram"""
        x_m = results["positions_mm"] / 1000
        deflections_mm = results["deflections_mm"]

        ax.plot(x_m, deflections_mm, "r-", linewidth=2, label="Deflection")
        ax.fill_between(x_m, 0, deflections_mm, alpha=0.3, color="red")

        # Mark maximum deflection
        max_idx = np.argmax(np.abs(deflections_mm))
        ax.plot(x_m[max_idx], deflections_mm[max_idx], "ro", markersize=8)
        ax.annotate(
            f"Max: {deflections_mm[max_idx]:.1f} mm",
            xy=(x_m[max_idx], deflections_mm[max_idx]),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        )

        # Add deflection limit line
        limit_mm = results["deflection_limit_mm"]
        ax.axhline(
            y=-limit_mm,
            color="orange",
            linestyle="--",
            label=f"Deflection Limit: {limit_mm:.1f} mm",
        )

        ax.set_xlabel("Position (m)")
        ax.set_ylabel("Deflection (mm)")
        ax.set_title("Deflection Diagram")
        ax.grid(True, alpha=0.3)
        ax.legend()

    def _plot_gate_elevation(
        self, ax, gate_width_mm: float, section: BeamSection
    ) -> None:
        """Plot gate elevation with dimensions"""
        # Convert to meters for plotting
        width_m = gate_width_mm / 1000
        height_m = 2.4  # Standard gate height

        # Draw gate frame
        gate_rect = Rectangle(
            (0, 0),
            width_m,
            height_m,
            linewidth=3,
            edgecolor="black",
            facecolor="lightgray",
            alpha=0.5,
        )
        ax.add_patch(gate_rect)

        # Draw main structural members
        member_width = section.width_mm / 1000
        member_height = section.depth_mm / 1000

        # Top rail
        top_rail = Rectangle(
            (0, height_m - member_height),
            width_m,
            member_height,
            linewidth=2,
            edgecolor="blue",
            facecolor="blue",
            alpha=0.7,
        )
        ax.add_patch(top_rail)

        # Bottom rail
        bottom_rail = Rectangle(
            (0, 0),
            width_m,
            member_height,
            linewidth=2,
            edgecolor="blue",
            facecolor="blue",
            alpha=0.7,
        )
        ax.add_patch(bottom_rail)

        # Vertical members
        n_verticals = int(width_m / 1.5) + 1  # Vertical every 1.5m
        for i in range(n_verticals):
            x_pos = i * width_m / (n_verticals - 1)
            vertical = Rectangle(
                (x_pos - member_width / 2, 0),
                member_width,
                height_m,
                linewidth=2,
                edgecolor="blue",
                facecolor="blue",
                alpha=0.7,
            )
            ax.add_patch(vertical)

        # Add dimensions
        ax.annotate(
            "",
            xy=(0, -0.3),
            xytext=(width_m, -0.3),
            arrowprops=dict(arrowstyle="<->", color="red", lw=2),
        )
        ax.text(
            width_m / 2,
            -0.4,
            f"{gate_width_mm:.0f} mm",
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
            color="red",
        )

        ax.annotate(
            "",
            xy=(-0.3, 0),
            xytext=(-0.3, height_m),
            arrowprops=dict(arrowstyle="<->", color="red", lw=2),
        )
        ax.text(
            -0.4,
            height_m / 2,
            f"{height_m * 1000:.0f} mm",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="red",
            rotation=90,
        )

        ax.set_xlim(-0.6, width_m + 0.2)
        ax.set_ylim(-0.6, height_m + 0.2)
        ax.set_aspect("equal")
        ax.set_xlabel("Length (m)")
        ax.set_ylabel("Height (m)")
        ax.set_title("Gate Elevation View")
        ax.grid(True, alpha=0.3)

    def _create_summary_text(self, results: Dict, section: BeamSection) -> str:
        """Create summary text for the analysis"""
        summary = f"""STRUCTURAL ANALYSIS SUMMARY
        
Section: {section.name}
Max Moment: {results["max_moment_Nmm"] / 1e6:.1f} kN⋅m
Max Stress: {results["max_stress_Pa"] / 1e6:.1f} MPa
Allowable Stress: {results["allowable_stress_Pa"] / 1e6:.1f} MPa
Stress Ratio: {results["stress_ratio"]:.2f}

Max Deflection: {results["max_deflection_mm"]:.1f} mm
Deflection Limit: {results["deflection_limit_mm"]:.1f} mm
Deflection Ratio: {results["deflection_ratio"]:.2f}

Safety Status: {"ADEQUATE" if results["safety_adequate"] else "INADEQUATE"}"""

        return summary

    def create_material_optimization_plot(
        self,
        sections: List[BeamSection],
        analysis_results: List[Dict],
        output_path: str,
    ) -> None:
        """Create material optimization comparison plot"""

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        section_names = [s.name for s in sections]
        weights = [s.area_mm2 * 6000 / 1000 for s in sections]  # kg for 6m beam
        stress_ratios = [r["stress_ratio"] for r in analysis_results]
        deflection_ratios = [r["deflection_ratio"] for r in analysis_results]
        costs = [w * 0.8 for w in weights]  # Estimated cost in USD/kg

        # Weight comparison
        bars1 = ax1.bar(section_names, weights, color="skyblue", edgecolor="navy")
        ax1.set_ylabel("Weight (kg)")
        ax1.set_title("Section Weight Comparison")
        ax1.tick_params(axis="x", rotation=45)

        # Add value labels on bars
        for bar, weight in zip(bars1, weights):
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{weight:.0f} kg",
                ha="center",
                va="bottom",
            )

        # Stress ratio comparison
        bars2 = ax2.bar(
            section_names, stress_ratios, color="lightcoral", edgecolor="darkred"
        )
        ax2.axhline(y=1.0, color="red", linestyle="--", label="Unity (Limit)")
        ax2.set_ylabel("Stress Ratio")
        ax2.set_title("Stress Utilization")
        ax2.tick_params(axis="x", rotation=45)
        ax2.legend()

        # Deflection ratio comparison
        bars3 = ax3.bar(
            section_names, deflection_ratios, color="lightgreen", edgecolor="darkgreen"
        )
        ax3.axhline(y=1.0, color="red", linestyle="--", label="Unity (Limit)")
        ax3.set_ylabel("Deflection Ratio")
        ax3.set_title("Deflection Utilization")
        ax3.tick_params(axis="x", rotation=45)
        ax3.legend()

        # Cost comparison
        bars4 = ax4.bar(section_names, costs, color="gold", edgecolor="orange")
        ax4.set_ylabel("Estimated Cost (USD)")
        ax4.set_title("Material Cost Comparison")
        ax4.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
