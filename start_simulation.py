from src import *
import time
import copy
import multiprocessing as mp

def run_single_configuration(config_number):
        # Initialize a new brush
        original_brush = brush.Brush()

        # Generate new Starting positions
        original_brush.initialize_positions()

        for temperature in TEMPERATURES:
            for c_interation in C_INTERACTIONS:  
                
                # Run the Monte Carlo for both types of Brush
                for is_block in [True, False]:
                    start_time = time.time()
                    brush_copy = copy.deepcopy(original_brush)
                    brush_copy.c_int = c_interation
                    brush_copy.set_type(is_block)
                    densities = run_monte_carlo(brush_copy, temperature)

                    #print(f"configuration:{config_number} nCint:{c_interation} temp:{temperature} is block:{is_block}")
                    #print(f"configuration:{config_number} nCint:{c_interation} \ntemp:{temperature} \nis block:{is_block} \nDensities: {densities}")
                    final_time = time.time() - start_time
                    #print(f"Simulation time: {final_time}")

def main():
    start_time = time.time()
    
    # Determine optimal number of processes based on CPU cores
    num_processes = min(STARTING_CONFIGURATIONS, mp.cpu_count())
    print(f"Starting parallel simulation with {num_processes} CPU cores...")
    
    # Create a process pool
    with mp.Pool(processes=num_processes) as pool:
        # Map configurations to processes and collect results
        all_results = []
        for result in pool.map(run_single_configuration, range(STARTING_CONFIGURATIONS)):
            if result is not None:
                all_results.extend(result)
    
    # Calculate total runtime
    total_runtime = time.time() - start_time

    print(f"All Monte Carlo simulations complete. \nTotal simulation runtime: {total_runtime}s")
    
    # Process and analyze results

if __name__ == "__main__":
    # Required for Windows systems
    mp.freeze_support()
    main() 
    