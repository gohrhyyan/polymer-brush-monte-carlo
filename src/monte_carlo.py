#def montecarlo(brush)
#excecutes the monte carlo simulation
"""
For 10^5 cycles:
    0) Calculate the energy of the system in the current state 
    1) Choose one particle at random
    2) Choose a random direction between (x,y,z)
    3) Choose a random displacement within the interval
    4) Calculate the difference in energy between the previous state and the one generated after the random displacement
    5) Choose a random number k between 0,1 If $\exp( - \Delta E / T ) < k$ then accept the new state, otherwise go back to the previous one. Every 1000 trials, save the positions of the particles at that point (you will need this information later). It does not matter if the move is accepted or not, a trial is considered every time an attempt is being made, not if successful.
"""