from src import *
import time
import copy
import multiprocessing as mp

def run_single_configuration(config_number):
        # Initialize a new instance of Brush class
        original_brush = brush.Brush()

        # Generate new Starting positions
        original_brush.initialize_positions()

        results = []


        for temperature in TEMPERATURES:
            for c_interation in C_INTERACTIONS:  
                # Run the Monte Carlo for both types of Brush, block and alternating
                for is_block in [True, False]:

                    # Create a deep copy of the original brush to preserve the initial state
                    brush_copy = copy.deepcopy(original_brush)

                    # Set the interaction constant for this simulation
                    brush_copy.c_int = c_interation

                    # Set the type of polymer, block or alternating for this simulation
                    brush_copy.set_type(is_block)

                    # Run the monte carlo simulation and get the densities
                    densities = run_monte_carlo(brush_copy, temperature)
                    
                    # TODO:save the result as a dictionary with the configuration to the results list. 

                    # Print that the simulation is complete
                    print(f"configuration:{config_number} nCint:{c_interation} temp:{temperature} is block:{is_block}")
                    

def main():
    # Record the overall start time of simulation
    start_time = time.time()
    
    # Determine optimal number of processes based on CPU cores
    num_system_cpu = mp.cpu_count()
    num_processes = min(STARTING_CONFIGURATIONS, num_system_cpu)
    print(f"Starting parallel simulation with {num_processes}/{num_system_cpu} CPU cores...")
    
    # Create a process pool
    with mp.Pool(processes=num_processes) as pool:

        # Initialize list to store all simulation results
        all_results = []

        # .map assigns a configuration number to each processor, and runs 1 configuration on each processor for the number of starting configurations there are
        # e.g, run_single_configuration(1), run_single_configuration(2)... run_single_configuration(STARTING_CONFIGURATIONS-1) 1 to each processor.
        # remaining tasks wait in a queue 
        for result in pool.map(run_single_configuration, range(STARTING_CONFIGURATIONS)):
                all_results.extend(result)
    
    # Calculate total runtime
    total_runtime = time.time() - start_time
    print(f"All Monte Carlo simulations complete. \nTotal simulation runtime: {total_runtime}s")

if __name__ == "__main__":
    # Enable multiprocessing support for windows
    mp.freeze_support()
    main() 
    