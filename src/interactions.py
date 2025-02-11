import numpy as np
from . import config

# calculates spring energy between two points
# inputs: two positions in space as [x,y,z]
# returns energy between the two points
def calc_spring_energy(pos1, pos2):
    spring_energy = 0.5 * config.K_SPRING * (np.linalg.norm(pos1 - pos2))**2
    return spring_energy


# calculates surface interaction energy from a particular height
# inputs, z vertical position value
# returns surface interaction energy
def calc_surface_energy(z):
    surface_energy = config.SURFACE_INTERACTION_ENERGY if z <= 0 else 0.0
    return surface_energy


# calculates the interaction energy between a reference particle and all other particles in the system 
# inputs: c_int (interaction constant), particle_positions (all positions), particle_types (A=1,B=-1), ref_chain_idx, ref_particle_idx (particle location indices), ref_particle_position (xyz position)
# returns total interation energy within radius config.R_SIZE
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
