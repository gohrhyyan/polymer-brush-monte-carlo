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
# returns: the surface interaction energy from the given z position
def calc_particle_interactions(c_int, particle_positions, particle_types, ref_chain_idx, ref_particle_idx, ref_particle_position):

    # Get the position and type of the reference particle from the arrays representing the entire brush.
    ref_particle_type = particle_types[ref_chain_idx, ref_particle_idx]    

    # initialize mask that exclcludes the reference particle
    # exclude the reference particle, as it cannot interact with itself
    ref_particle_mask = np.ones_like(particle_types, dtype=bool)
    ref_particle_mask[ref_chain_idx, ref_particle_idx] = False
    
    # calculate exact spherical distances between reference particle and the remaining particles
    distances = np.linalg.norm(particle_positions[ref_particle_mask] - ref_particle_position, axis=1)
    
    # mask out remaining particles outside interaction radius
    spherical_mask = distances < config.R_SIZE
    
    # calculate the interaction energy between each particle within the interaction sphere and the reference particle
    interaction_energies = (ref_particle_type * particle_types[ref_particle_mask][spherical_mask]) * c_int * np.cos((np.pi/2) * (distances[spherical_mask]/config.R_SIZE))
    
    total_interaction = np.sum(interaction_energies, dtype= config.PRECISION)
    
    return total_interaction
