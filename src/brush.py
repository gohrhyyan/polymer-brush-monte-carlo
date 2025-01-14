import numpy as np
import interactions
import config

#define class Brush, representing:
#    1) positions of each particle in each polymer chain.
#       3D numpy array: 
#       [chain index, particle index in chain, 3d coordiantes]

#    2) grafting position of each polymer chain.
#       2D numpy array:
#       [x,y]

class Brush: 
    def __init__(self):
        # use indexing to access the data for a given particle.
        
        """physical information""" 
        # Initialise 3d array to store particle positions for each chain.
        # (chain number, particle in chain, 3 xyz coords) 
        self.particle_pos = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN, 3))
        
        # Initialize a 2d array to store graft positions for each chain
        # (chain number, 2 xy coords)
        self.graft_pos = np.zeros((config.NUM_CHAINS, 2))

        # Initialize a 2d array to store type (A/B) for each particle
        # Type A will be equivilant to 1, type B will be equivilant to -1
        self.particle_type = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN))

        """energy cache"""
        # Stores of energy to reduce compute time.

        # Initialize a 2d array to store the energy of the spring BELOW each particle
        # (chain number, particle in chain) 
        self.spring_energy = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN))

        # Initialize a 2d array to store the energy of each particle's interaction with every other particle.
        self.particle_energy = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN))

        # Initialize a 2d array to store the energy of each particle's interaction with the surface.
        self.surface_energy = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN))

        #initialise a variable to store the total energy of the system
        self.total_energy = 0.0

        
    def initialize_positions(self):
        # to generate grafting coordinates:
        total_positions = config.BASE_LEN_X * config.BASE_LEN_Y

        # generate a numpy array of length config.NUM_CHAINS with random numbers from 0 and total_positions -1
        random_flat_indices = np.random.choice(total_positions, size=config.NUM_CHAINS, replace=False)

        # convert the array of numbers between 0 and total_positions into x and y coordinates.
        # see: https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
        x_coords = random_flat_indices % config.BASE_LEN_X
        y_coords = random_flat_indices // config.BASE_LEN_X

        #combine the x and y coordinates into a single 2d array and assign the grafting coordinates
        self.graft_pos = np.column_stack((x_coords, y_coords))

        # Assign grafting positions to all particles.
        # graft_pos is a 3d array with shape [config.NUM_CHAINS, config.CHAIN_LEN, 3], and particle_pos is a 2d array with shape [config.NUM_CHAINS, 2]
        # particles is indexed without the z-coordinate [:, :, :2] into shape [config.NUM_CHAINS, config.CHAIN_LEN, 2]
        # graft pos is indexed with an additonal axis [:, None, :] into shape [config.NUM_CHAINS, 1, 2]
        # numpy broadcasting copies the co-ordinate for each chain in graft_pos to all particles in particle_pos.
        self.particle_pos[:, :, :2] = self.graft_pos[:, None, :] 

        # assign z-positions
        # start from config.SPRING_START_LENGTH because it is the minimum height off grafting surface, which is at z = 0
        # np.arange(config.SPRING_START_LENGTH, config.CHAIN_LEN + 1) creates a 1d array starting from 1, ending at (CHAIN_LEN+1)*SPRING_START_LENGTH, with SPRING_START_LENGTH spacing
        # indexing self.particles[:, :, 2] referencess all z-axis values for all particles in all chains.
        # numpy broadcasting copies coordinates to all chains
        self.particle_pos[:, :, 2] = np.arange(config.SPRING_START_LENGTH, 
                                      (config.CHAIN_LEN + 1) * config.SPRING_START_LENGTH,
                                      config.SPRING_START_LENGTH)


        # assign x and y positions.
        # shape of graft_pos is (50 chains, 2 coordinates)
        # adding None converts the array into (50,1,2) meaning [50 chains, 1 particle, 2 coordinates (x,y)]
        # numpy broadcasting copies coordinates to all particles in each chain,
        # indexing :2 to set x,y coordinates only
        self.particle_pos[:, :, :2] = self.graft_pos[:, None, :]

        # if config.SPRING_START_LENGTH > 0, all particles are at z > 0 at the start, no particles are interacting with the surface.
        # otherwise, if config.SPRING_START_LENGTH <= 0 all particles are either on or inside the surface, and are interacting with the surface.
        # therefore the config.SPRING_START_LENGTH can be used with the calc_surface_energy() function to determine the starting surface interaction energy of all particles.
        self.surface_energy.fill(interactions.calc_surface_energy(config.SPRING_START_LENGTH))

        # therefore, all springs are the same length and have the same energy
        self.spring_energy.fill(interactions.calc_spring_energy(0, config.SPRING_START_LENGTH))

        """initialize particle interaction energy"""
        """calculate total energy"""
        #IMPT: Sum of all particle energy must be divided by 2 to avoid double counting
        

    def set_type(self, is_block):
        # initialize a new numpy array with chain length to store the desired type pattern
        target_pattern = np.zeros(config.CHAIN_LEN)
        
        # to generate a block pattern
        if is_block:
            # find the midpoint of the array using floor division (odd lengths will be split unevenly, A block will have 1 less than B block)
            mid = config.CHAIN_LEN // 2

            # assign the first half of the array to be 1 = A
            target_pattern[:mid] = 1

            # assign the second half of the array to be -1 = B
            target_pattern[mid:] = -1
        
        # to generate an alternating pattern 
        else:
            # use numpy tile to generate a repeating pattern of 1, -1 = A, B
            # repeat pattern for -(config.CHAIN_LEN // -2) repetitions
                # i.e add 1 more repetition if config.CHAIN_LEN is odd
            # trim pattern to the same length as config.CHAIN_LEN
            target_pattern = np.tile([1, -1], -(config.CHAIN_LEN // -2))[:config.CHAIN_LEN]
        
        # set all particle chains to use the target type pattern
        self.particle_type[:] = target_pattern
        