from src import *
import copy

def main():
    print("Initialising System")
    
    #Randomly assign the bases for 50 polymer chains onto the square grid of 10LX10L where L=1 (100 possible positions)
        #Enter for loop, 50 times
        #If the point selected is already occupied, regenerate random position

    #Generate each chain, as a system of 10 particles.
    #Note, this needs to be done for 2 types of system, alternating copolymer and diblock copolymer
        #For each coordinate in BASES
            #Enter For loop 10 times
                #All particles in a chain must have the same x and y position
                #All particles in the chain are seperated by a unit of 1 in the z axis
"""

For 10 different initial configurations of the system:
    For 3 values of interaction constant C=-0.5,-1 (for attractive particles) and 0.5,1 for repulsive particles:
        For 3 different temperatures: T=0.5, 1 and 2:
            Excecute the Monte Carlo Simulation monte_carlo.py
""" 

if __name__ == "__main__":
    main() 

    #use copy.deepcopy(brush class instance) to prevent "crosstalk" pointer screwups