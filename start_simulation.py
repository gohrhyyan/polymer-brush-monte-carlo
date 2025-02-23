from src import *
import time
import copy
import multiprocessing as mp

# get the half the total number of saves made, for calculating equilibrium density.
half_saves = int(TIMES_TO_SAVE/2)

# funtion to run monte-carlo simulations for a new starting configuration, for each temperature, c_int, and polymer type.
# args: config_index (just a unique identifier integer)
# returns: dictionary of results for all configurations.
def run_single_configuration(config_index):
        
    # Initialize a new instance of Brush class
    original_brush = brush.Brush()

    # initialize a new random number generator for this configuration, using the config_index as the seed.
    # fixes: all results being the same due to time based-rng having the same values for all initial configurations.
    rng = np.random.default_rng(config_index)

    # Generate new Starting positions
    original_brush.initialize_positions(rng)

    results = []
    
    for temperature in TEMPERATURES:
        for c_int in C_INTERACTIONS:
            # Run the Monte Carlo for both types of Brush, block and alternating
            for is_block in [True, False]:

                # Create a deep copy of the original brush to preserve the initial state
                brush_copy = copy.deepcopy(original_brush)

                # Set the interaction constant for this simulation
                brush_copy.c_int = c_int

                # Set the type of polymer, block or alternating for this simulation
                brush_copy.set_type(is_block)

                # Run the monte carlo simulation and get the densities
                densities = run_monte_carlo(brush_copy, temperature, rng)

                # Calculate equilibrium statistics using last 50,000 steps (50 save points)
                equilibrium_density = np.mean(densities[-half_saves:])
                equilibrium_variance = np.var(densities[-half_saves:])
                               
                results.append({
                    "c_int" : c_int,
                    "temperature" : temperature,
                    "is_block" : is_block,
                    "densities" : densities,
                    "equilibrium_density": equilibrium_density,
                    "equilibrium_variance" : equilibrium_variance
                })
                
                # Print that the simulation is complete
                print(f"Configuration:{config_index} Interaction Constant:{c_int} Temperature:{temperature} Is block:{is_block}")

    # Return structure:
    #   {
    #     "config_index": int,                 # Index identifying the initial configuration
    #     "results": [{
    #         "c_int": float,                  # Interaction parameter
    #         "temperature": float,            # Temperature parameter
    #         "is_block": bool,                # True for block polymer, False for alternating
    #         "densities": List[float],        # List of density values at each save point
    #         "equilibrium_density": float,    # Final equilibrium density
    #         "equilibrium_variance": float    # Variance in equilibrium density
    #       },
    #       ...more results for different parameter sets with the same initial configuration, 12 total...
    #      ]
    #   }
    return {"config_index" : config_index,
            "results" : results}
    
                    

def main():
    # Record the overall start time of simulation
    start_time = time.time()
    
    # Determine optimal number of processes based on CPU cores
    # Assign one starting configuration to one CPU core, whichever is less.
    num_system_cpu = mp.cpu_count()
    num_processes = min(STARTING_CONFIGURATIONS, num_system_cpu)
    print(f"Starting parallel simulation with {num_processes}/{num_system_cpu} CPU cores...")
    
    # Create a process pool to handle parallel processing
    with mp.Pool(processes=num_processes) as pool:

        # Initialize list to store all dictionaries of simulation results
        all_results = []

        # .map assigns a configuration number to each processor, and runs 1 configuration on each processor for the number of starting configurations there are
        # e.g, run_single_configuration(1), run_single_configuration(2)... run_single_configuration(STARTING_CONFIGURATIONS-1) 1 to each processor.
        # remaining tasks wait in a queue 
        # return from run_single_configuration is stored the list of all_results
        # all_results: List[Dict]
        # [{
        #     "config_index": int,
        #     "results": [{
        #         "c_int": float,
        #         "temperature": float,
        #         "is_block": bool,                
        #         "densities": List[float],
        #         "equilibrium_density": float,
        #         "equilibrium_variance": float 
        #     },
        #     ...more results for different parameter sets with the same initial configuration, 12 total...
        #    ]
        #  },
        # ...more different initial configurations 10 total...
        # ]
        for configuration_results in pool.map(run_single_configuration, range(STARTING_CONFIGURATIONS)):
                all_results.append(configuration_results)
                
    
        
    # Calculate total runtime
    total_runtime = time.time() - start_time
    print(f"All Monte Carlo simulations complete. \nTotal simulation runtime: {total_runtime}s")

    # generate graphs and csv file
    print(f"Exporting results to {config.RESULTS_FOLDERNAME}...")
    plot_and_save_data(all_results)
    print(f"complete.")

if __name__ == "__main__":
    # Enable multiprocessing support for windows
    mp.freeze_support()
    main() 
    