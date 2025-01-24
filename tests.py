import interactions
import numpy as np

particle_positions = np.array([[[ 6, 3, 1],  [ 6, 3, 2],  [ 6, 3, 3]], [[ 5, 2, 1],  [ 9, 6.2, 1.9],  [ 5, 2, 3]], [[ 9, 6, 1.5],  [ 9, 6, 2],  [ 9, 6, 2.5]], [[ 0, 6, 1],  [ 0, 6, 2],  [ 0, 6, 3]]])
particle_types = np.array([[ 1, -1, 1],[ 1, -1, 1],[ 1, -1, 1],[ 1, -1, 1]])

ref_chain_idx = 2
ref_particle_in_chain_idx = 1

print(interactions.calc_particle_interactions(particle_positions, particle_types, ref_chain_idx, ref_particle_in_chain_idx))

"""
new_brush = brush.Brush()
new_brush.initialize_positions()
new_brush.set_type(is_block = False)

print(new_brush.particle_positions)
print(new_brush.particle_types)
"""