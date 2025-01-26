import matplotlib.pyplot as plt
from . import config
import numpy as np

#Data for number of steps (x) and equilibrium densities (y)
def plotting(banana):
    x = [i for i in range(1000, 10**5 + 1, 1000)] #since this is here, we only need to update the y axis with new data 
    y = banana

    #Plotting the data
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Equilibrium Density')

    #Adding labels and title
    plt.xlabel('Number of Steps', fontsize=12)
    plt.ylabel('Equilibrium Density of Particles', fontsize=12)
    plt.title('Equilibrium Density vs. Number of Steps', fontsize=14)
    plt.grid(True)

    #Display legend
    plt.legend()

    #Show the plot
    plt.show()


