import numpy as np
import config

# np.linalg.norm() is a function that calculates the magnitude of the distance between two points, eqivilant to pythagoras theorem

# calculates spring energy between two points
def calc_spring_energy(pos1, pos2):
    return 0.5 * config.K_SPRING * (np.linalg.norm(pos1 - pos2))**2

# calculates surface interaction energy
def calc_surface_energy(z):
    return config.SURFACE_INTERACTION_ENERGY if z <= 0 else 0.0

# calculates particle interaction energy
    # type1 and type2 are the particle types: 1 or -1 corresponding to A or B respectively
def calc_particle_interaction(type1, type2, pos1, pos2):
    dist = np.linalg.norm(pos1 - pos2)
    if dist < config.R_SIZE:
        # like types, AA or BB 11 or -1-1 will = 1 when multiplied, for the positive cint in repulsive interactions 
        # unlike types, AB or BA 1-1 or -11 will = -1 when multiplied, for the negative cint in attractive interactions 
        return (type1 * type2) * config.C_INTERACTION * np.cos((np.pi/2) * (dist/config.R_SIZE))
    return 0.0


   
def calc_particle_interactions(particle_positions, particle_types, ref_chain_idx, ref_particle_in_chain_idx):

    ref_particle_position = particle_positions[ref_chain_idx, ref_particle_in_chain_idx]
    ref_particle_type = particle_types[ref_chain_idx, ref_particle_in_chain_idx]
    
    # initialise a boolean mask array with the same shape as particle_positions
    # mask will help to exclude particles not under analysis
    mask = np.ones_like(particle_types, dtype=bool)

    # exclude the reference particle, as we are not 
    mask[ref_chain_idx, ref_particle_in_chain_idx] = False
    
    # use a "bounding box" to reduce the number of particles that need to be analysised
    # progressively mask out particles that are outside the bounding box along each axis
    for axis in range(3):
        mask[mask] = np.abs(particle_positions[mask][:,axis] - ref_particle_position[axis]) <= config.R_SIZE
    
    #  calculate distances between reference particle and the remaining particles inside the bounding box
    diff = particle_positions - ref_particle_position
    distances = np.linalg.norm(diff, axis=2)  
    
    # mask out remaining particles outside interaction radius
    mask = mask & (distances < config.R_SIZE)
    
    interaction_energies = (ref_particle_type * particle_types[mask]) * config.C_INTERACTION * \
                         np.cos((np.pi/2) * (distances[mask]/config.R_SIZE))
    
    total_interaction = np.sum(interaction_energies)
    
    return total_interaction
