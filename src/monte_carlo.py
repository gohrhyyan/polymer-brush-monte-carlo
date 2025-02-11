import numpy as np
from . import config

# function to put a brush through a single monte carlo simulation (i.e 10^5 iterations)
# inputs: class brush that has been initialized, temperature for this run.
# return: 1d array of densities calculated at every config.ITERATIONS_BETWEEN_SAVES iterations (i.e 1000 iterations)
def run_monte_carlo(brush, temperature):
    # initialize array to store particle positions at save points
    # shape: (number of save_points, number of chains, number of particles per chain, xyz_coords)
    saved_positions = np.zeros((config.TIMES_TO_SAVE, 
                              config.NUM_CHAINS,
                              config.CHAIN_LEN,
                              3), dtype=config.PRECISION)
    
    # monte carlo simulation runs for 1000 steps on the inner loop, escapes to the outer loop to save current positions in saved_positions, then goes back into the inner loop.
    for save_number in range(config.TIMES_TO_SAVE):
        for iteration in range(config.ITERATIONS_BETWEEN_SAVES):
            # randomly select a chain and particle.
            chain_idx = np.random.randint(0, config.NUM_CHAINS)
            particle_idx = np.random.randint(0, config.CHAIN_LEN)
            
            # generate a random move direction and magnitude.
            move_direction = np.random.randint(0, 3)  # x, y, or z
            move_magnitude = np.random.uniform(-1, 1)
            
            # Calculate energy difference for proposed move
            delta_e = brush.test_move(chain_idx, particle_idx, move_direction, move_magnitude)
            
            # calculate the acceptance criteria
            if np.random.random() < np.exp(-delta_e / temperature):
                brush.accept_move()
    
        # save the current particle positions for density calculation later
        saved_positions[save_number] = brush.particle_positions
    
    # Calculate the volume for density calculation
    volume = config.BASE_LEN_Y * config.BASE_LEN_X * config.DENSITY_CALC_Z_BOUNDARY

    # Flag z-coordinates that are below than or equal to the z_boundary
    mask = saved_positions[..., 2] <= config.DENSITY_CALC_Z_BOUNDARY

    # Sum over all chains and particles for each save point
    # densities is a 1d array of the calculated near-surface density at each save point. config.length = TIMES_TO_SAVE
    densities = np.sum(mask, axis=(1, 2)) / volume

    return densities

