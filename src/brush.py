import numpy as np
#define class Brush, representing:
#    1) positions of each particle in each polymer chain.
#       3D numpy array: 
#       [chain index, particle index in chain, 3d coordiantes]

#    2) grafting position of each polymer chain.
#       2D numpy array:
#       [x,y]

class Brush: 
    def __init__(self, NUM_CHAINS=50, CHAIN_LEN=10, BASE_LEN_X=10, BASE_LEN_Y=10):

        self.NUM_CHAINS = NUM_CHAINS  # Number of polymer chains
        self.CHAIN_LEN = CHAIN_LEN    # Length of each polymer chain
        self.BASE_LEN_X = BASE_LEN_X  # Number of grid points in the X direction
        self.BASE_LEN_Y = BASE_LEN_Y  # Number of grid points in the Y direction

        # Initialise 3d array to store particle positions for each chain.
        # (NUM_CHAINS, CHAIN_LEN, 3 xyz coords) 
        self.particles = np.zeros((NUM_CHAINS, CHAIN_LEN, 3))
        
        # Initialize an array to store graft positions for each chain
        # (NUM_CHAINS, 2 xy coords)
        self.graft_pos = np.zeros((NUM_CHAINS, 2))

        # use indexing to access the grafing position for a particular chain. 

        
    def initialize_brush(self):
        # to generate grafting coordinates:
        # generate a random array of numbers from 0 to 99, without replacement.
        # number in 10s place = x axis position
        # number in 1s place = y axis position
        coords = np.random.choice(100, size=50, replace=False)

        # Assign the coordinates to the chains, using the grafting position array
        # split the digits into valid coordinates:
        #   floor division by 10 to get the x coordinate in the 10s place
        #   modulo by 10 to get the y coordinate in the 1s place
        self.graft_pos = np.column_stack((coords // 10, coords % 10))

        # Assign positions to all particles.
        self.particles[:, :, :2]
        # assign z-positions
        # starting with 1 for the first particle in the chain, incrementing by 1 for every subsequent particle in the same chain
        # start from 1 because it is not possible for a polymer to be on the grafting surface, which is at z = 0
        # np.arange(1, self.CHAIN_LEN + 1) function creates a 1D array starting from 1, ending at CHAIN_LEN+1 .
        # indexing self.particles[:, :, 2] referencess all z-axis values for all particles in all chains.
        # numpy broadcasting copies coordinates to all chains
        self.particles[:, :, 2]  = np.arange(1, self.CHAIN_LEN + 1)

        # assign x and y positions.
        # shape of graft_pos is (50 chains, 2 coordinates)
        # adding None converts the array into (50,1,2) meaning [50 chains, 1 particle, 2 coordinates (x,y)]
        # numpy broadcasting copies coordinates to all particles in each chain,
        # indexing :2 to set x,y coordinates only
        self.particles[:, :, :2] = self.graft_pos[:, None, :]

        # uncomment these 2 lines to view coordinates (for debugging)
        # for chain in self.particles:
        #   print(chain)









    