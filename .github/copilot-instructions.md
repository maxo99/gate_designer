<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Cantilever Slide Gate Design Project Instructions

This is a structural engineering project for designing cantilever slide gates. When working on this project:

## Engineering Standards
- Use metric units (mm, N, Pa) unless otherwise specified
- Follow structural engineering best practices and safety factors
- Apply relevant building codes and standards (AISC, AWS, etc.)
- Use appropriate safety factors for structural calculations (typically 2.0-3.0)

## Code Style
- Use clear, descriptive variable names for engineering parameters
- Include units in variable names or comments (e.g., `load_N`, `moment_Nmm`)
- Document all calculations with references to engineering principles
- Use type hints for all functions dealing with engineering calculations

## Design Process
- Always validate input parameters for physical reasonableness
- Include error handling for impossible geometries or loads
- Generate warnings for designs that approach safety limits
- Provide clear output with engineering significance

## Documentation
- Include calculation references and assumptions
- Generate professional-quality technical documentation
- Use proper engineering notation and symbols
- Include material properties and design criteria in outputs

## Reference Design Integration
- When working with the Tymetal Fortress reference design, maintain structural principles
- Scale designs proportionally while checking structural adequacy
- Flag any modifications that may affect structural integrity
- Use proven connection details and reinforcement patterns
