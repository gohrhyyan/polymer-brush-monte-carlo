import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from . import config


# function to save the plot to a file
# args: filename: str, name of the file to save the plot to
#       graph_title: str, title of the graph to display
# stores: the plot to the filename specified
# return: none
def save_plot(filename, graph_title):
    # Add axis labels and title
    plt.xlabel('Number of Steps', fontsize=12)
    plt.ylabel('Density (particles/volume)', fontsize=12)
    plt.title(graph_title, fontsize=14)
    
    # Add a legend and grid
    plt.legend(loc='best', fontsize=8)
    plt.grid(True, alpha=0.3)

    # save the figure for all configurations in this parameter set.
    plt.savefig(filename)
    plt.close()



# function to plot and save the graphs to png files, and save the data to a csv file
# args:  all_results: List[Dict] is a list of dictionaries containing the results for each initial configuration, packaged at start_simulation.py
#   [{
#     "config_index": int,                 # Index identifying the initial configuration
#     "results": [{                        # List of results 
#         "c_int": float,                  # Interaction parameter
#         "temperature": float,            # Temperature parameter
#         "is_block": bool,                # True for block polymer, False for alternating
#         "densities": List[float],        # List of density values at each save point
#         "equilibrium_density": float,    # Final equilibrium density
#         "equilibrium_variance": float    # Variance in equilibrium density
#       },
#       ...more results for different parameter sets for the same configuration...
#      ]
#    }
#   ...more configurations
#   ]
# stores: the individual configuration plots and combined parameter plots as png files, and the data to a csv file to the results folder
# return: none
def plot_and_save_data(all_results):
    # Create a dictionary to sort data according to simulation parameters (unique combination of c_int, temperature and is_block).
    parameter_combinations = {}
    
    # Generate the x-axis values (number of iterations)
    x_axis_values = np.arange(      
        0,                                                                  # Start at the 0, initial configuration
        (config.ITERATIONS_BETWEEN_SAVES * config.TIMES_TO_SAVE) + 1,       # End at the total number of iterations. +1 to handle arange behavior which does not include the final point by default
        config.ITERATIONS_BETWEEN_SAVES                                     # Step size between saves
    )

    # Create the results directory if it doesn't exist
    os.makedirs(config.RESULTS_FOLDERNAME, exist_ok=True)

    # Initialize a csv file
    with open(config.CSV_FILENAME, 'w', newline='') as csvfile:

        # Create CSV writer and write header to the CSV file
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Configuration', 'Type', 'Temperature', 'C_int', 'Equilibrium Density', 'Variance'])
         
        # Unpack data to show trends for each combination of parameters
        # Index into the results for each initial configuration
        # configuration: {config_index, results[dict}}
        for configuration in all_results:
        
            # Unpack the parameters for each configuration
            # result: {c_int, temperature, is_block, densities[float], equilibrium_density, equilibrium_variance}
            for result in configuration["results"]:

                # Create a string from the polymer_type boolean for output
                polymer_type = "Block" if result["is_block"] else "Alternating"

                # Write the configuration, parameters, and results to the CSV
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

                # Create density against iterations
                # Make line graph
                plt.plot(x_axis_values, result["densities"], marker='', linestyle='-', label=f'Config {configuration["config_index"]}', alpha=0.7)

                # Add equilibruim density and variance text box
                plt.text(0.02, 0.98, f'Equilibrium Density: {result["equilibrium_density"]:.4f}\nVariance: {result["equilibrium_variance"]:.4f}',
                    transform=plt.gca().transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
                )

                # Generate the graph title and filename
                graph_title = f'{config.GRAPH_TITLE} \n{polymer_type} Polymer, T={result["temperature"]}, C_int={result["c_int"]}'
                filename = f'{config.RESULTS_FOLDERNAME}/{configuration["config_index"]}_density_plot_{polymer_type}_T{result["temperature"]}_C{result["c_int"]}.png'

                # save the figure for this configuration and parameter set.
                save_plot(filename, graph_title)

                # Pack the data for later plotting in overall results graphs, where initial configurations with the same parameters are plotted as different lines on the same graph.
                # Create a key for this parameter combination
                key = (result["c_int"], result["temperature"], polymer_type)
                
                # Initialize this parameter combination if it doesn't exist
                if key not in parameter_combinations:
                    parameter_combinations[key] = {}
                
                # Add the data for this configuration, and this index to the dictionary, according to this parameter combination
                # parameter_combinations is a dictionary of dictionaries, containing data for each configuration with the same set of parameters.
                # parameter_combinations: Dict[Tuple: Dict]
                # Structure:
                # {   # Key is the tuple of matching parameters
                #     (c_int, temperature, polymer_type): {
                #           config_index: {                   # Key is configuration index
                #             'densities': List[float],       # List of density values
                #             'equilibrium_density': float,   # Final equilibrium density
                #             'equilibrium_variance': float   # Variance in equilibrium density
                #         },
                #         ...more configurations with the same parameters
                #     }
                # }
                parameter_combinations[key][configuration["config_index"]] = {
                    'densities': result["densities"],
                    'equilibrium_density': result["equilibrium_density"],
                    'equilibrium_variance': result["equilibrium_variance"]
                    }

    # Create a plot for each parameter combination
    # get the key tuple and value ductionary as seperate variables
    # key: (c_int, temperature, polymer_type)
    # config_data: {config_index: {densities, equilibrium_density, equilibrium_variance},...}
    for key, config_data in parameter_combinations.items():

        # Unpack parameters from key tuple
        c_int, temperature, polymer_type = key
        
        # Create a new figure for this parameter combination
        plt.figure(figsize=(10, 6))
        
        # Average the equilibrium densities and variance statistics for the results in each set of parameters
        mean_equilibrium_density = np.mean([data['equilibrium_density'] for data in config_data.values()])
        mean_equilibrium_variance = np.mean([data['equilibrium_variance'] for data in config_data.values()])
    
        # Plot each configuration's densities in a different color
        # unpack the config index identifier from the nested dictionary key
        # config_index: int
        # data: {densities[float], equilibrium_density, equilibrium_variance}
        for config_index, data in config_data.items():
            plt.plot(x_axis_values, data['densities'], marker='', linestyle='-', label=f'Config {config_index}', alpha=0.7)

        # Add text box with mean values
        plt.text(0.02, 0.98, 
                f'Mean Equilibrium Density: {mean_equilibrium_density:.4f}\n' + 
                f'Mean Equilibrium Variance: {mean_equilibrium_variance:.4f}',
                transform=plt.gca().transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
        # save the figure for all configurations in this parameter set.
        graph_title = f'{config.GRAPH_TITLE}\n{polymer_type} Polymer, T={temperature}, C_int={c_int}'
        filename = f'{config.RESULTS_FOLDERNAME}/overall_{polymer_type}_T{temperature}_C{c_int}.png'
        save_plot(filename, graph_title)




