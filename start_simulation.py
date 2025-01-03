#Project structure:
#
# polymer_simulation/
# ├── src/
# │   ├── __init__.py
# │   ├── particle.py        # Particle class and related functions
# │   ├── spring.py          # Spring energy calculations
# │   ├── interactions.py    # Particle interaction calculations
# │   ├── polymer.py         # Polymer chain class
# │   ├── monte_carlo.py     # Monte Carlo simulation steps
# │   └── utils.py           # Utility functions (energy calcs, etc)
# └── start_simulation.py    # Main entry point

def main():
    print("Initialising Simulation")
    #Randomly assign the bases for 50 polymer chains onto the square grid of 10LX10L where L=1 (100 possible positions)
        #Enter for loop, 50 times
        #If the point selected is already occupied, regenerate random position

    #Generate each chain, as a system of 10 particles.
    #Note, this needs to be done for 2 types of system, alternating copolymer and diblock copolymer
        #For each coordinate in BASES
            #Enter For loop 10 times
                #All particles in a chain must have the same x and y position
                #All particles in the chain are seperated by a unit of 1 in the z axis

    #
    

if __name__ == "__main__":
    main()