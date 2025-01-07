import numpy as np
#define class Brush, representing:
#    1) positions of each particle in each polymer chain.
#       3D numpy array: 
#       [chain index, particle index in chain, 3d coordiantes]

#    2) grafting position of each polymer chain.
#       2D numpy array:
#       [x,y]

class Brush: 
    def __init__(self, NUM_CHAINS, CHAIN_LEN, BASE_LEN_X, BASE_LEN_Y):

        self.NUM_CHAINS = NUM_CHAINS  # Number of polymer chains
        self.CHAIN_LEN = CHAIN_LEN    # Length of each polymer chain
        self.BASE_LEN_X = BASE_LEN_X  # Number of grid points in the X direction
        self.BASE_LEN_Y = BASE_LEN_Y  # Number of grid points in the Y direction

        # Initialise 3d array to store particle positions for each chain.
        # (NUM_CHAINS, CHAIN_LEN, 3 xyz coords) 
        self.particles = np.zeros((NUM_CHAINS, CHAIN_LEN, 3))
        
        # Initialize an array to store graft positions for each chain
        # Shape: (NUM_CHAINS, 2 xy coords)
        self.graft_pos = np.zeros((NUM_CHAINS, 2))

        # use indexing to access the grafing position for a particular chain. 

        
    def initialize_brush(self):
        # generate a random array of numbers from 0 to 99, without replacement.
        coords = np.random.choice(100, size=50, replace=False)

        # split the digits into valid coordinates:
        #   floor division by 10 for the x coordinate in the 10s position
        #   modulo by 10 for the y coordinate in the 1s position
        self.graft_pos = np.column_stack((coords // 10, coords % 10))


        #assign this to the z values for each molecule
        #np.arange(1,self.CHAIN_LEN+1)


        








    