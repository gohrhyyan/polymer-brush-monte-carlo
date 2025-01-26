import numpy as np
from . import config

# excecutes the monte carlo simulation
NEAR_SURFACE_VOLUME = config.BASE_LEN_Y * config.BASE_LEN_X * config.DENSITY_CALC_Z_BOUNDARY
def calc_density(brush):
    mask = brush.particle_positions[:, :, 2] <= config.DENSITY_CALC_Z_BOUNDARY
    density = np.sum(mask) / NEAR_SURFACE_VOLUME
    return density


def run_monte_carlo(brush, temperature):
    # Main Monte Carlo loop
    saved_surface_densities = np.zeros(config.TIMES_TO_SAVE, dtype = config.PRECISION)
    for save_number in range(config.TIMES_TO_SAVE):
        for iteration in range(config.ITERATIONS_BETWEEN_SAVES):
            # randomly select a particle
            chain_idx = np.random.randint(0, config.NUM_CHAINS)
            particle_idx = np.random.randint(0, config.CHAIN_LEN)
            
            # generate a random move
            move_direction = np.random.randint(0, 3)  # x, y, or z
            move_magnitude = np.random.uniform(-1, 1)
            
            # Calculate energy difference for proposed move
            delta_e = brush.test_move(chain_idx, particle_idx, move_direction, move_magnitude)
            
            # acceptance criteria
            if np.random.random() > np.exp(-delta_e / temperature):
                brush.accept_move()
    
        current_surface_density = calc_density(brush)
        print(current_surface_density)
        saved_surface_densities[save_number] = current_surface_density
    
    return saved_surface_densities

