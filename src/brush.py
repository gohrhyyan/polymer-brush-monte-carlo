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

        # use indexing to access the data for a given particle.
        """physical information""" 
        # Initialise 3d array to store particle positions for each chain.
        # (chain number, particle in chain, 3 xyz coords) 
        self.particle_pos = np.zeros((NUM_CHAINS, CHAIN_LEN, 3))
        
        # Initialize a 2d array to store graft positions for each chain
        # (chain number, 2 xy coords)
        self.graft_pos = np.zeros((NUM_CHAINS, 2))

        # Initialize a 2d array to store type (A/B) for each particle
        # Type A will be equivilant to 1, type B will be equivilant to -1
        self.particle_type = np.zeros((NUM_CHAINS, CHAIN_LEN))

        """energy cache"""
        # Stores of energy to reduce compute time.

        # Initialize a 2d array to store the energy of the spring BELOW each particle
        # (chain number, particle in chain) 
        self.spring_energy = np.zeros((NUM_CHAINS, CHAIN_LEN))

        # Initialize a 2d array to store the energy of each particle's interaction with every other particle.
        self.particle_energy = np.zeros((NUM_CHAINS, CHAIN_LEN))

        # Initialize a 2d array to store the energy of each particle's interaction with the surface.
        self.surface_energy = np.zeros((NUM_CHAINS, CHAIN_LEN))

        #initialise a variable to store the total energy of the system
        self.total_energy = 0.0

        
    def initialize_positions(self):
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
        self.particle_pos[:, :, 2]  = np.arange(1, self.CHAIN_LEN + 1)

        # assign x and y positions.
        # shape of graft_pos is (50 chains, 2 coordinates)
        # adding None converts the array into (50,1,2) meaning [50 chains, 1 particle, 2 coordinates (x,y)]
        # numpy broadcasting copies coordinates to all particles in each chain,
        # indexing :2 to set x,y coordinates only
        self.particle_pos[:, :, :2] = self.graft_pos[:, None, :]

        # uncomment these 2 lines to view coordinates (for debugging)
        # for chain in self.particles:
        #   print(chain)

        #loop over all particles

            #calculate particle interaction energy, update cache
            #calculate spring energy, update cache
            #calculate surface energy, update cache
        
        """calculate total energy"""

    def set_type(self, is_block):
        # initialize a new numpy array with chain length to store the desired type pattern
        target_pattern = np.zeros(self.CHAIN_LEN)
        
        # to generate a block pattern
        if is_block:
            # find the midpoint of the array using floor division (odd lengths will be split unevenly, A block will have 1 less than B block)
            mid = self.CHAIN_LEN // 2

            # assign the first half of the array to be 1 = A
            target_pattern[:mid] = 1

            # assign the second half of the array to be -1 = B
            target_pattern[mid:] = -1
        
        # to generate an alternating pattern 
        else:
            # use numpy tile to generate a repeating pattern of 1, -1 = a, b
            # repeat pattern for -(self.CHAIN_LEN // -2) repetitions
                # i.e add 1 more repetition if CHAIN_LEN is odd
            # trim pattern to the same length as CHAIN_LEN
            target_pattern = np.tile([1, -1], -(self.CHAIN_LEN // -2))[:self.CHAIN_LEN]
        
        self.particle_type[:] = target_pattern
        