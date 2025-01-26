import numpy as np
from . import config

# calculates spring energy between two points
def calc_spring_energy(pos1, pos2):
    if(config.VERBOSE): print(f"Interactions.py, calc_spring_energy started, received positions: pos1: {pos1},  pos2:{pos2}")
    spring_energy = 0.5 * config.K_SPRING * (np.linalg.norm(pos1 - pos2))**2
    if(config.VERBOSE): print(f"Interactions.py, calc_spring_energy calcualted spring energy: {spring_energy}")
    return spring_energy


# calculates surface interaction energy
def calc_surface_energy(z):
    if(config.VERBOSE): print(f"Interactions.py, calc_surface_energy started, received z: {z}")
    surface_energy = config.SURFACE_INTERACTION_ENERGY if z <= 0 else 0.0
    if(config.VERBOSE): print(f"Interactions.py, calc_surface_energy calcualted surface energy: {surface_energy}")
    return surface_energy


# calculates the interaction energy between a reference particle and all other particles in the system 
def calc_particle_interactions(particle_positions, particle_types, ref_chain_idx, ref_particle_idx, ref_particle_position):
    if(config.VERBOSE): print(f"""
Interactions.py, calc_particle_interactions started.
Particle positions array:\n{particle_positions}\n
Particle types array:\n{particle_types}\n
Reference chain index: {ref_chain_idx}
Reference particle in chain index: {ref_particle_idx}
Reference particle position: {ref_particle_position},""")

    # Get the position and type of the reference particle from the arrays representing the entire brush.
    ref_particle_type = particle_types[ref_chain_idx, ref_particle_idx]    
    if(config.VERBOSE): print(f"Interactions.py, calc_particle_interactions retrieved reference particle type:{ref_particle_type}")
    
    # use a "bounding box" to reduce the number of particles that need to be analysised
    # calculate smallest and largest possible x,y,z co-ordinates:
    box_min = ref_particle_position - config.R_SIZE
    box_max = ref_particle_position + config.R_SIZE

    # initialize mask that exclcludes particles outside bounding box, all particles start as True, inside the bounding box
    bounding_box_mask = np.ones_like(particle_types, dtype=bool)
    
    # mask out particles that are outside the bounding box along each axis
    # if the particle is outside the boundning box: update mask to false
    # Particles already masked as false are not repeated, using bounding_box_mask[bounding_box_mask]
    #for axis in range(3): 
        #bounding_box_mask[bounding_box_mask] = (box_min[axis] <= particle_positions[bounding_box_mask][:, axis]) & (particle_positions[bounding_box_mask][:, axis] <= box_max[axis])
# ^^^ THIS ACTUALLY MAKES IT SLOWER

    # exclude the reference particle, as it cannot interact with itself
    bounding_box_mask[ref_chain_idx, ref_particle_idx] = False
    if(config.VERBOSE): print(f"Interactions.py, calc_particle_interactions set reference particle to false:\n{bounding_box_mask}\n")
    
    # calculate exact spherical distances between reference particle and the remaining particles inside the bounding box
    distances = np.linalg.norm(particle_positions[bounding_box_mask] - ref_particle_position, axis=1)
    
    # mask out remaining particles outside interaction radius
    spherical_mask = distances < config.R_SIZE
    
    # calculate the interaction energy between each particle within the interaction sphere and the reference particle
    interaction_energies = (ref_particle_type * particle_types[bounding_box_mask][spherical_mask]) * config.C_INTERACTION * np.cos((np.pi/2) * (distances[spherical_mask]/config.R_SIZE))
    
    total_interaction = np.sum(interaction_energies, dtype= config.PRECISION)
    
    return total_interaction
