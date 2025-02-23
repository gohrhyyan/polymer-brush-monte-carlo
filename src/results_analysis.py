import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from . import config

def save_plot(filename, graph_title):
    # Add labels and title with parameter information
    plt.xlabel('Number of Steps', fontsize=12)
    plt.ylabel('Density (particles/volume)', fontsize=12)
    plt.title(graph_title, fontsize=14)
    
    # Add a legend and grid
    plt.legend(loc='best', fontsize=8)
    plt.grid(True, alpha=0.3)

    # save the figure for all configurations in this parameter set.
    plt.savefig(filename)
    plt.close()


def plot_and_save_data(all_results):
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

    # Initialize CSV file 
    csv_filename = 'results/simulation_results.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        # Create CSV writer and write header
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Configuration', 'Type', 'Temperature', 'C_int', 'Equilibrium Density', 'Variance'])
        

        # Index into the results for each initial configuration
        for configuration in all_results:
        
            # Unpack the parameters for each configuration
            for result in configuration["results"]:

                polymer_type = "Block" if result["is_block"] else "Alternating"

                # Write to CSV
                csvwriter.writerow([
                    configuration["config_index"],
                    polymer_type,
                    result["temperature"],
                    result["c_int"],
                    f"{result['equilibrium_density']:.6f}",
                    f"{result['equilibrium_variance']:.6f}"
                ])

                # Create a new figure for this parameter combination
                plt.figure(figsize=(10, 6))

                # Plot density against iterations graph
                plt.plot(x, result["densities"], marker='', linestyle='-', label=f'Config {configuration["config_index"]}', alpha=0.7)
                plt.text(0.02, 0.98, f'Equilibrium Density: {result["equilibrium_density"]:.4f}\nVariance: {result["equilibrium_variance"]:.4f}',
                transform=plt.gca().transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

                # save the figure for this configuration and parameter set.
                graph_title = f'Surface Density vs. Steps \n{polymer_type} Polymer, T={result["temperature"]}, C_int={result["c_int"]}'
                filename = f'results/{configuration["config_index"]}_density_plot_{polymer_type}_T{result["temperature"]}_C{result["c_int"]}.png'
                save_plot(filename, graph_title)
                    
                # Create a key for this parameter combination
                key = (result["c_int"], result["temperature"], result["is_block"])
                
                # Initialize this parameter combination if it doesn't exist
                if key not in parameter_combinations:
                    parameter_combinations[key] = {}
                
                # Add the densities for this configuration, and this index to the dictionary, according to this parameter combination
                parameter_combinations[key][configuration["config_index"]] = {
                    'densities': result["densities"],
                    'equilibrium_density': result["equilibrium_density"],
                    'equilibrium_variance': result["equilibrium_variance"]
                    }

    
    # Create a plot for each parameter combination
    for key, config_data in parameter_combinations.items():

        #Unpack parameters for display
        c_int, temperature, is_block = key
        polymer_type = "Block" if is_block else "Alternating"
        
        # Create a new figure for this parameter combination
        plt.figure(figsize=(10, 6))
        
        # Plot each configuration's densities and collect equilibrium statistics
        mean_equilibrium_density = np.mean([data['equilibrium_density'] for data in config_data.values()])
        mean_equilibrium_variance = np.mean([data['equilibrium_variance'] for data in config_data.values()])
    
        # Plot each configuration's densities in a different color
        for config_index, data in config_data.items():
            plt.plot(x, data['densities'], marker='', linestyle='-', label=f'Config {config_index}', alpha=0.7)

        # Add text box with mean values
        plt.text(0.02, 0.98, 
                f'Mean Equilibrium Density: {mean_equilibrium_density:.4f}\n' + 
                f'Mean Equilibrium Variance: {mean_equilibrium_variance:.4f}',
                transform=plt.gca().transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
        # save the figure for all configurations in this parameter set.
        graph_title = f'Surface Density vs. Steps\n{polymer_type} Polymer, T={temperature}, C_int={c_int}'
        filename = f'results/overall_density_plot_{polymer_type}_T{temperature}_C{c_int}.png'
        save_plot(filename, graph_title)




