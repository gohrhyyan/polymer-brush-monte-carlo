# ic-python-groupproj
Project structure:

polymer_simulation/
├── src/
│   ├── __init__.py
│   ├── brush.py          # Polymer brush class
│   ├── monte_carlo.py     # Monte Carlo simulation steps
│   ├── config.py
│   └── interactions.py    # energy calculations
└── start_simulation.py    # Main entry point

Please note Python conventions as defined in PEP 8 (Python's official style guide):

snake_case:
- Function names: `calculate_energy()`, `monte_carlo_step()`
- Variable names: `particle_count`, `total_energy`
- Method names: `calculate_spring_energy()`
- Module names: `monte_carlo.py`, `interactions.py`

PascalCase:
- Class names: `Particle`, `PolymerChain`, `Brush`
- Exception names: `ValueError`, `TypeError`
- Type variable names: `ParticleType`, `ChainType`

SCREAMING_SNAKE_CASE (all uppercase):
- Constants: `MAX_ITERATIONS = 100000`, `SPRING_CONSTANT = 1.0`