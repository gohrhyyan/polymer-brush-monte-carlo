"""
Polymer Simulation Package
"""

# Import main classes and functions that should be available when importing the package
from .brush import Particle, PolymerChain, Brush
from .monte_carlo import montecarlo
from .interactions import calculate_spring_energy, calculate_interaction_energy, calculate_surface_energy, calculate_total_energy

# Package metadata
__version__ = '0.1.0'
__author__ = 'Your Name'

# Define what should be available when using `from src import *`
__all__ = [
    'Particle',
    'PolymerChain',
    'Brush',
    'montecarlo',
    'calculate_spring_energy',
    'calculate_interaction_energy',
    'calculate_surface_energy',
    'calculate_total_energy'
]