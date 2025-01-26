from src import *
import time

def main():
    print("Initialising System")
    start_time = time.time()
    new_brush = brush.Brush()
    new_brush.initialize_positions()
    new_brush.set_type(is_block = True)
    run_monte_carlo(new_brush, 1)
    final_time = time.time() - start_time
    print(final_time)

"""

For 10 different initial configurations of the system:
    For 3 values of interaction constant C=-0.5,-1 (for attractive particles) and 0.5,1 for repulsive particles:
        For 3 different temperatures: T=0.5, 1 and 2:
            Excecute the Monte Carlo Simulation monte_carlo.py
""" 

if __name__ == "__main__":
    main() 

    #use copy.deepcopy(brush class instance) to prevent "crosstalk" pointer screwups
    