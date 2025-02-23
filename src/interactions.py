import numpy as np
from . import config

# function to calculate spring energy between two points
# args: two arrays of co-ordinates [x,y,z]
# returns: the calculated spring energy between the two points
def calc_spring_energy(pos1, pos2):
    # numpy implementation of the spring formula $E_{spring}(ij) = {1\over2} \,k\, d_{ij}^2$
    spring_energy = 0.5 * config.K_SPRING * (np.linalg.norm(pos1 - pos2))**2
    return spring_energy

# function to calculate surface interaction energy
# args: z axis poisition value of the particle
# returns: the surface interaction energy from the given z position
def calc_surface_energy(z):
    #implementation of $E_{surf}(i) = 10^9$
    surface_energy = config.SURFACE_INTERACTION_ENERGY if z <= 0 else 0.0
    return surface_energy

# function to calculate the interaction energy between a reference particle and all other particles in the system 
# args: 
    # c_int: interaction constant
    # particle_positions: 3d Numpy array of particle position data: (chain number, particle in chain, xyz coords)
    # particle_types: 2d array to store type (A/B) for each particle. A = 1, B = -1
    # ref_chain_idx, ref_particle_idx: chain and particle indexes of the reference particle
    # ref_particle_position: [x,y,z] coordinates of the reference particle
# returns: 2D array of shape (NUM_CHAINS, CHAIN_LEN) containing energy contributions from each particle to the reference particle
def calc_particle_interactions(c_int, particle_positions, particle_types, ref_chain_idx, ref_particle_idx, ref_particle_position):

    # Get the type (A=1 or B=-1) of the reference particle.
    ref_particle_type = particle_types[ref_chain_idx, ref_particle_idx]    

    # Initialize array to store energy contributions for each particle
    # Same shape as particle_types: (NUM_CHAINS, CHAIN_LEN)
    energy_contributions = np.zeros_like(particle_types, dtype=config.PRECISION)
    
    # calculate exact spherical distances between reference particle and the remaining particles
    # particle_positions shape: (NUM_CHAINS, CHAIN_LEN, 3) where 3 is (x,y,z)
    # axis=2 tells np.linalg.norm to calculate along the xyz coordinates,
    # distances shape: (NUM_CHAINS, CHAIN_LEN)
    distances = np.linalg.norm(particle_positions - ref_particle_position, axis=2)
    
    # mask out remaining particles outside interaction radius
    spherical_mask = distances < config.R_SIZE
    
    # calculate the interaction energy between each particle within the interaction sphere and the reference particle
    energy_contributions[spherical_mask] = (ref_particle_type * particle_types[spherical_mask]) * c_int * np.cos((np.pi/2) * (distances[spherical_mask]/config.R_SIZE))

    # Zero out self-interaction
    energy_contributions[ref_chain_idx, ref_particle_idx] = 0
    
    return energy_contributions
