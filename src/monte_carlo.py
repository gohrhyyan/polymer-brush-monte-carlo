import brush
import numpy as np
import time
import config
import density_calculation
import plots
# excecutes the monte carlo simulation
y = []

def run_monte_carlo(brush, temperature, num_steps):
    # Main Monte Carlo loop
    for step in range(num_steps):
        # Randomly select a particle
        chain_idx = np.random.randint(0, config.NUM_CHAINS)
        particle_idx = np.random.randint(0, config.CHAIN_LEN)
        
        # Generate random move
        move_direction = np.random.randint(0, 3)  # x, y, or z
        move_magnitude = np.random.uniform(-1, 1)
        
        # Calculate energy difference for proposed move
        delta_E = brush.test_move(chain_idx, particle_idx, move_direction, move_magnitude)
        
        # Metropolis criterion
        if delta_E <= 0 or np.random.random() < np.exp(-delta_E / temperature):
            brush.accept_move()
    
    
    
start_time = time.time()
new_brush = brush.Brush()
new_brush.initialize_positions()

new_brush.set_type(is_block = True)
for i in range(100):
    run_monte_carlo(new_brush, 1, num_steps=1000)
   #banana = density_calculation.calcdensity(new_brush)
    #print(banana)
    #y.append(banana)
final_time = time.time() - start_time
print(final_time)
#plots.plotting(y)