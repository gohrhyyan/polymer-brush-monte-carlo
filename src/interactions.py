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

def calc_particle_interactions(particle_positions, particle_types, key_particle_idx):
    #key_particle_idx = a 1d list of [chain index, particle in chain index]
    #particle_positions = self.particle_pos from brush
    #particle_types = self. particle_type from bush

    #create a mask that will be used across particle pos and particle type 

    #get the particle pos and particle type of the particle index particle_idx and store them as variables
    #key_particle_position = 
    #key_particle_type = 

    #mask out particle_idx from particle_positions and particle_types

    #distances = np.linalg.norm(particle_position - key_particle_positon)

    #mask out particles that are further away than R_SIZE while maintaining the previous mask of particle_idx

    # Calculate interactions where mask is True

    # Sum all interactions