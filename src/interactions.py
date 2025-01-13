import numpy as np

# calculates spring energy between two points
def calc_spring_energy(pos1, pos2, K_SPRING):
    return 0.5 * K_SPRING * (np.linalg.norm(pos1 - pos2))**2

# calculates surface interaction energy
def calc_spring_energy(z):
    return 1e9 if z < 0 else 0.0

# calculates particle interaction energy
    # type1 and type2 are the particle types: 1 or -1 corresponding to A or B respectively

def calc_particle_interaction(type1, type2, pos1, pos2, C_INTERACTION, R_SIZE):
    dist = np.linalg.norm(pos1 - pos2)
    if dist < R_SIZE:
        # like types, AA or BB 11 or -1-1 will = 1 when multiplied, for the positive cint in repulsive interactions 
        # unlike types, AB or BA 1-1 or -11 will = -1 when multiplied, for the negative cint in attractive interactions 
        return (type1 * type2) * C_INTERACTION * np.cos((np.pi/2) * (dist/R_SIZE))
    return 0.0