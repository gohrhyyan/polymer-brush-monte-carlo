import numpy as np
from . import interactions
from . import config

#define class Brush, containing all information about the current state of the polymer brush, and methods to modify the state of the brush
class Brush: 
    
    # method to initialize variables that store brush position and energy information.
    # args: self
    # no return value
    # stores: empty arays/variables for state and energy information
    def __init__(self):
        # use indexing to access the data for a given particle.
        """physical information""" 
        # Initialise 3d array to store particle positions for each chain.
        # (chain number, particle in chain, xyz coords) 
        self.particle_positions = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN, 3), dtype= config.PRECISION)
        
        # Initialize a 2d array to store graft positions for each chain
        # (chain number, xyz coords) where z is always 0
        self.graft_positions = np.zeros((config.NUM_CHAINS, 3), dtype= config.PRECISION)

        # Initialize a 2d array to store type (A/B) for each particle
        # Type A will be equivilant to 1, type B will be equivilant to -1
        self.particle_types = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        # Initialize a List to store information about any pending moves
        self.pending_move = None

        # Initialize an interaction constant for this Brush
        self.c_int = 0

        """energy cache""" 
        # Stores of energy to reduce compute time.
        # Initialize a 2d array to store the energy of the spring BELOW each particle
        # (chain number, particle in chain) 
        self.spring_energies = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        # Initialize a 4d array to store the energy contribution that each particle contributes to each other particle
        # i.e pairwise interaction energies
        # Shape: (chain1, particle1, chain2, particle2)
        # interaction_cache[i,j,k,l] represents energy contribution between 
        # particle j in chain i and particle l in chain k
        self.interaction_cache = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN, 
                                         config.NUM_CHAINS, config.CHAIN_LEN), 
                                         dtype=config.PRECISION)

        # Initialize a 2d array to store the energy of each particle's interaction with the surface.
        self.surface_energies = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        #initialise a variable to store the total energy of the system
        self.total_energy = 0.0

    # method to generate random grafting points and vertical chain positions
    # args: self, rng - numpy random number generator object.
    # no return value
    # stores: postitional information of an initialized brush.
    def initialize_positions(self, rng):
        # get the total number of positions on the grafting surface
        total_positions = config.BASE_LEN_X * config.BASE_LEN_Y

        # generate a numpy array of length config.NUM_CHAINS (50 for the challenge)
        # populate with random numbers from 0 to (total_positions -1)
        random_flat_indices = rng.choice(total_positions, size=config.NUM_CHAINS, replace=False)

        # convert the random array of numbers between 0 and total_positions into x and y coordinates.
        # see: https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
        x_coords = random_flat_indices % config.BASE_LEN_X
        y_coords = random_flat_indices // config.BASE_LEN_X

        # combine the x and y coordinates into a single array and assign the grafting coordinates
        # assign 0 to all z coords as the grafting surface is at z = 0
        # graft_positions shape: (NUM_CHAINS, 3) where 3 is (x,y,z)
        self.graft_positions = np.column_stack((x_coords, y_coords, np.zeros(config.NUM_CHAINS, dtype=config.PRECISION)))

        # assign grafting x,y positions to all particles.
        # particle_positions is a 3d array with shape [config.NUM_CHAINS, config.CHAIN_LEN, 3], and graft_positions is a 2d array with shape [config.NUM_CHAINS, 3]
        # particles are indexed without the z-coordinate [:, :, :2] into shape [config.NUM_CHAINS, config.CHAIN_LEN, 2]
        # graft pos is indexed with an additional dimension for the particles in the chain and limited to x,y coordinates [:, None, :2] into shape [config.NUM_CHAINS, 1, 2]
        # numpy broadcasting copies the x,y coordinates for each chain in graft_positions to all particles in particle_positions.
        self.particle_positions[:, :, :2] = self.graft_positions[:, None, :2] 

        # assign z-positions to all particles
        # start from config.SPRING_START_LENGTH because it is the minimum height off grafting surface, which is at z = 0
        # np.arange(config.SPRING_START_LENGTH, config.CHAIN_LEN + 1) creates a 1d array starting from config.SPRING_START_LENGTH, ending at (CHAIN_LEN+1)*SPRING_START_LENGTH, with SPRING_START_LENGTH spacing
        # indexing self.particles[:, :, 2] referencess all z-axis values for all particles in all chains.
        # numpy broadcasting copies coordinates to all chains
        self.particle_positions[:, :, 2] = np.arange(config.SPRING_START_LENGTH, 
                                                    (config.CHAIN_LEN + 1) * config.SPRING_START_LENGTH,
                                                    config.SPRING_START_LENGTH, dtype= config.PRECISION)

    # method to calculate the initial energy of the brush (only works with initial position configuration.)
    # args: self
    # no return value
    # stores: energy information of an initialized brush.
    def initialize_energies(self):
        # if config.SPRING_START_LENGTH > 0, all particles are at z > 0 at the start, no particles are interacting with the surface.
        # otherwise, if config.SPRING_START_LENGTH <= 0 all particles are either on or inside the surface, and are interacting with the surface.
        # therefore the config.SPRING_START_LENGTH can be used with the calc_surface_energy() function to determine the starting surface interaction energy of all particles.
        self.surface_energies.fill(interactions.calc_surface_energy(config.SPRING_START_LENGTH))

        # all springs start at the same length and have the same energy
        self.spring_energies.fill(interactions.calc_spring_energy(np.array([0,0,0]), np.array([0,0,config.SPRING_START_LENGTH])))

        # initialize pairwise interaction cache
        # loop through all particles in all chains
        for ref_chain_idx in range(config.NUM_CHAINS):
            for ref_particle_idx in range(config.CHAIN_LEN):
                # calculate interactions for this particle
                self.interaction_cache[ref_chain_idx, ref_particle_idx] = interactions.calc_particle_interactions(
                    self.c_int,
                    self.particle_positions,
                    self.particle_types,
                    ref_chain_idx,
                    ref_particle_idx,
                    ref_particle_position = self.particle_positions[ref_chain_idx, ref_particle_idx]
                )

        # calculate total energy      
        # IMPT: Sum of all particle energy must be divided by 2 to avoid double counting
        self.total_energy = np.sum(self.spring_energies) + np.sum(self.surface_energies) + (np.sum(self.interaction_cache) / 2)

    # method to set the type of the polymer brush, block or alternating
    # args: self, is_block boolean indicating if the chain is to be block or not.
    # no return value
    # stores: particle type information
    def set_type(self, is_block):
        # initialize a new numpy array with same length as chain length to store the desired type pattern
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
                # i.e if config.CHAIN_LEN is odd, use an extra repetition to ensure the pattern is long enough.
                # using upside down floor division. see: https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
            # trim pattern to the same length as config.CHAIN_LEN using [:config.CHAIN_LEN]
            target_pattern = np.tile([1, -1], -(config.CHAIN_LEN // -2))[:config.CHAIN_LEN]
        
        # set all particles to follow the  target type pattern
        self.particle_types[:] = target_pattern
    
    
    # method to calculate state of brush after move, without altering the brush.
    # args: self, 
        # ref_chain_idx, ref_particle_idx chain and particle indexes of the particle to be moved and tested
        # move_dir, move_magnitude direction of and magnitiude of the move to be tested
    # returns: delta_e
    # stores: move information waiting for accept_move() call.
    def test_move(self, ref_chain_idx, ref_particle_idx, move_dir, move_magnitude):
        # retrive a copy of the current reference particle position
        new_pos = self.particle_positions[ref_chain_idx, ref_particle_idx].copy()

        # increment the coordinate of the single axis by the magnitude
        new_pos[move_dir] += move_magnitude

        # initialise a bool to indicate if the reference particle is the last particle in the chain. (avoids checking again later)
        # if the reference particle index (0 indexed) is equal to (chain length - 1), (1 indexed) then the reference particle is the last particle in the chain.
        # this prevents index out of bounds errors and also prevents attempts to calculate energy against non-existant particles
        is_last = (ref_particle_idx == config.CHAIN_LEN - 1)

        # initialise a bool to indicate if the reference particle is the first particle in the chain. (avoids checking again later)
        # if the reference particle index (0 indexed) is equal to 0 then the reference particle is the first particle in the chain.
        # if true, the spring below calculation will be against the grafting point.
        is_first = (ref_particle_idx == 0)
        
        # get the current energies from the energy cache
        old_spring_above = 0 if is_last else self.spring_energies[ref_chain_idx, ref_particle_idx + 1]
        old_spring_below = self.spring_energies[ref_chain_idx,ref_particle_idx]
        old_surface = self.surface_energies[ref_chain_idx,ref_particle_idx]
        old_interaction_contributions = self.interaction_cache[ref_chain_idx, ref_particle_idx]

        # calculate the new energies with the new particle position, using the interactions functions
        new_spring_above = 0 if is_last else interactions.calc_spring_energy(new_pos, self.particle_positions[ref_chain_idx, ref_particle_idx + 1])
        new_spring_below = interactions.calc_spring_energy(new_pos, self.graft_positions[ref_chain_idx]) if is_first else interactions.calc_spring_energy(new_pos, self.particle_positions[ref_chain_idx, ref_particle_idx - 1]) 
        new_surface = interactions.calc_surface_energy(new_pos[2])
        new_interaction_contributions = interactions.calc_particle_interactions(self.c_int, self.particle_positions,self.particle_types,ref_chain_idx,ref_particle_idx, ref_particle_position=new_pos)
        
        # calculate the total delta e
        delta_e = ((new_spring_above - old_spring_above) +  # where spring_above is 0 for last particle
            (new_spring_below - old_spring_below) + 
            (new_surface - old_surface) + 
            (np.sum(new_interaction_contributions) - np.sum(old_interaction_contributions)))

        # store the calculated energies and reference particle information as a pending move
        self.pending_move = [is_last, ref_chain_idx, ref_particle_idx, new_spring_above, new_spring_below, new_surface, new_interaction_contributions, delta_e, new_pos]

        # return the delta_e to the monte carlo simulation
        return delta_e

    # method to update the brush state to the recently checked move
    # args: self
    # no return value
    # stores: new positional and energy information
    def accept_move(self):
        # update class energies and positions with information in self.pending_move
        # unpack pending move information
        is_last, ref_chain_idx, ref_particle_idx, new_spring_above, new_spring_below, new_surface, new_interaction_contributions, delta_e, new_pos = self.pending_move
        
        # Update particle position
        self.particle_positions[ref_chain_idx, ref_particle_idx] = new_pos

        # Update cached energies for the moved particle
        # Only update the energy for the spring above if the particle is not the last in the chain.
        if not is_last: self.spring_energies[ref_chain_idx, ref_particle_idx + 1] = new_spring_above
        self.spring_energies[ref_chain_idx, ref_particle_idx] = new_spring_below
        self.surface_energies[ref_chain_idx, ref_particle_idx] = new_surface
        
        # Update interaction cache in both directions of the symmetrical interaction
        # interaction_cache is a 4D array with shape: (NUM_CHAINS, CHAIN_LEN, NUM_CHAINS, CHAIN_LEN)
        # where interaction_cache[i,j,k,l] represents energy contribution between:
        #   - particle j in chain i (source particle)
        #   - particle l in chain k (target particle)

        # new_interaction_contributions is a 2D array with shape: (NUM_CHAINS, CHAIN_LEN) containing energy contributions between the moved particle and all other particles
        # We don't only need to update the moved particle's 2d slice, but also the 2d slice of all other particles that have interactions with the moved particle.
        # Each particle has their own 2d slice in the interaction_chache that represents the energy they have with all other particles.

        # Update outgoing interactions: 
        # To update how much energy the moved particle contributes to all other particles:
        # - Slice the 4D interaction_cache by fixing first two dimensions to [ref_chain_idx, ref_particle_idx] indexing the moved particle's 2d slice
        # - This Slice represents the interaction energy that the moved particle has with all other particles.
        # - This gives a 2D slice with shape (NUM_CHAINS, CHAIN_LEN) representing energy FROM moved particle TO all others
        self.interaction_cache[ref_chain_idx, ref_particle_idx] = new_interaction_contributions

        
        # Update incoming interactions: 
        # To update how much energy other particles contribute to the moved particle:
        # - Slice the 4D interaction_cache by fixing last two dimensions to [ref_chain_idx, ref_particle_idx] indexing the moved particle in all other particles' 2d slices
        # - Select all values for first two dimensions using [:, :]
        # - This gives a 2D slice with shape (NUM_CHAINS, CHAIN_LEN) representing energy TO moved particle FROM all others
        self.interaction_cache[:, :, ref_chain_idx, ref_particle_idx] = new_interaction_contributions

        # Update total system energy
        self.total_energy += delta_e

        # Clear the stored pending move
        self.pending_move = None
