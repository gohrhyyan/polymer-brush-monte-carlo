import matplotlib.pyplot as plt
import numpy as np
import os
from . import config

def plot_graphs(all_results):
    # Unpack data to show trends for each combination of parameters
    # Create a dictionary to sort data according to simulation parameters (unique combination of c_int, temperature and is_block).
    parameter_combinations = {}
    
    # Generate the x-axis values (number of iterations)
    x = np.arange(      
    0,                                                                  # Start at the 0, initial configuration
    (config.ITERATIONS_BETWEEN_SAVES * config.TIMES_TO_SAVE) + 1,       # End at the total number of iterations. +1 to handle arange behavior which does not include the final point by default
    config.ITERATIONS_BETWEEN_SAVES                                     # Step size between saves
    )

    # Create the results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)

    # Index into the results for each initial configuration
    for config_result in all_results:
    
        # Unpack the parameters for each configuration
        for result in config_result["results"]:

            # Create a new figure for this parameter combination
            plt.figure(figsize=(10, 6))
            
            # Plot each configuration's densities in a different color
            plt.plot(x, result["densities"], marker='', linestyle='-', label=f'Config {config_result["config_index"]}', alpha=0.7)
                
            # Add labels and title with parameter information
            polymer_type = "Block" if result["is_block"] else "Alternating"
            plt.xlabel('Number of Steps', fontsize=12)
            plt.ylabel('Density (particles/volume)', fontsize=12)
            plt.title(f'Surface Density vs. Steps\n{polymer_type} Polymer, T={result["temperature"]}, C_int={result["c_int"]}', fontsize=14)
            
            # Add a legend and grid
            plt.legend(loc='best', fontsize=8)
            plt.grid(True, alpha=0.3)

            # save the figure for this configuration and parameter set.
            plt.savefig(f'results/{config_result["config_index"]}_density_plot_{polymer_type}_T{result["temperature"]}_C{result["c_int"]}.png')
            plt.close()

            # Create a key for this parameter combination
            key = (result["c_int"], result["temperature"], result["is_block"])
            
            # Initialize this parameter combination if it doesn't exist
            if key not in parameter_combinations:
                parameter_combinations[key] = {}
            
            # Add the densities for this configuration, and this index to the dictionary, according to this parameter combination
            parameter_combinations[key][config_result["config_index"]] = result["densities"]

    
    # Create a plot for each parameter combination
    for key, config_densities in parameter_combinations.items():

        #Unpack parameters for display
        c_int, temperature, is_block = key
        polymer_type = "Block" if is_block else "Alternating"
        
        # Create a new figure for this parameter combination
        plt.figure(figsize=(10, 6))
        
        # Plot each configuration's densities in a different color
        for config_index, densities in config_densities.items():
            plt.plot(x, densities, marker='', linestyle='-', 
                     label=f'Config {config_index}', alpha=0.7)
            
        # Add labels and title with parameter information
        plt.xlabel('Number of Steps', fontsize=12)
        plt.ylabel('Density (particles/volume)', fontsize=12)
        plt.title(f'Surface Density vs. Steps\n{polymer_type} Polymer, T={temperature}, C_int={c_int}', 
                 fontsize=14)
        
        # Add a legend and grid
        plt.legend(loc='best', fontsize=8)
        plt.grid(True, alpha=0.3)

        # save the figure for all configurations in this parameter set.
        plt.savefig(f'results/overall_density_plot_{polymer_type}_T{temperature}_C{c_int}.png')
        plt.close()


