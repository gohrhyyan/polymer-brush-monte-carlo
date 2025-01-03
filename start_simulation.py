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

#define the class: system.
    #The polymer brush system is a list of 10 class polymer chain

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
0) Calculate the energy of the system $E_{tot}$ in the current state 
1) Choose one particle at random
2) Choose a random direction between (x,y,z)
3) Choose a random displacement within the interval $(-1,1)$
4) Calculate the difference in energy between the previous state and the one generated after the random displacement
5) Choose a random number between $[0,1)$, let's call it $k$. If $\exp( - \Delta E / T ) < k$ then accept the new state, otherwise go back to the previous one. Every 1000 trials, save the positions of the particles at that point (you will need this information later). It does not matter if the move is accepted or not, a trial is considered every time an attempt is being made, not if successful.
6) Go back to step 1) and reiterate this algorithm.

Repeat the previous loop (0-6) for $10^5$ iterations.
You also need to repeat this simulation for 10 different initial configurations of the system.
You should also repeat this experiment for 3 different temperatures: T=0.5, 1 and 2 
3 different values of the interaction constant C=-0.5,-1 (for attractive particles) and 0.5,1 for repulsive particles.
""" 

if __name__ == "__main__":
    main()