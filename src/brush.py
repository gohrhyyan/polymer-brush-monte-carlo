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
        self.particle_positions = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN, 3), dtype= config.PRECISION)
        
        # Initialize a 2d array to store graft positions for each chain
        # (chain number, 2 xy coords)
        self.graft_positions = np.zeros((config.NUM_CHAINS, 2), dtype= config.PRECISION)

        # Initialize a 2d array to store type (A/B) for each particle
        # Type A will be equivilant to 1, type B will be equivilant to -1
        self.particle_types = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        # Initialize a List to store information about any pending moves
        self.pending_move = None


        """energy cache""" # Stores of energy to reduce compute time.
        # Initialize a 2d array to store the energy of the spring BELOW each particle
        # (chain number, particle in chain) 
        self.spring_energies = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        # Initialize a 2d array to store the energy of each particle's interaction with every other particle.
        self.particle_energies = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

        # Initialize a 2d array to store the energy of each particle's interaction with the surface.
        self.surface_energies = np.zeros((config.NUM_CHAINS, config.CHAIN_LEN), dtype= config.PRECISION)

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
        self.graft_positions = np.column_stack((x_coords, y_coords))

        # Assign grafting positions to all particles.
        # graft_positions is a 3d array with shape [config.NUM_CHAINS, config.CHAIN_LEN, 3], and particle_positions is a 2d array with shape [config.NUM_CHAINS, 2]
        # particles is indexed without the z-coordinate [:, :, :2] into shape [config.NUM_CHAINS, config.CHAIN_LEN, 2]
        # graft pos is indexed with an additonal axis [:, None, :] into shape [config.NUM_CHAINS, 1, 2]
        # numpy broadcasting copies the co-ordinate for each chain in graft_positions to all particles in particle_positions.
        self.particle_positions[:, :, :2] = self.graft_positions[:, None, :] 

        # assign z-positions
        # start from config.SPRING_START_LENGTH because it is the minimum height off grafting surface, which is at z = 0
        # np.arange(config.SPRING_START_LENGTH, config.CHAIN_LEN + 1) creates a 1d array starting from 1, ending at (CHAIN_LEN+1)*SPRING_START_LENGTH, with SPRING_START_LENGTH spacing
        # indexing self.particles[:, :, 2] referencess all z-axis values for all particles in all chains.
        # numpy broadcasting copies coordinates to all chains
        self.particle_positions[:, :, 2] = np.arange(config.SPRING_START_LENGTH, 
                                      (config.CHAIN_LEN + 1) * config.SPRING_START_LENGTH,
                                      config.SPRING_START_LENGTH, dtype= config.PRECISION)

        # assign x and y positions.
        # shape of graft_positions is (50 chains, 2 coordinates)
        # adding None converts the array into (50,1,2) meaning [50 chains, 1 particle, 2 coordinates (x,y)]
        # numpy broadcasting copies coordinates to all particles in each chain,
        # indexing :2 to set x,y coordinates only
        self.particle_positions[:, :, :2] = self.graft_positions[:, None, :]

        # if config.SPRING_START_LENGTH > 0, all particles are at z > 0 at the start, no particles are interacting with the surface.
        # otherwise, if config.SPRING_START_LENGTH <= 0 all particles are either on or inside the surface, and are interacting with the surface.
        # therefore the config.SPRING_START_LENGTH can be used with the calc_surface_energy() function to determine the starting surface interaction energy of all particles.
        self.surface_energies.fill(interactions.calc_surface_energy(config.SPRING_START_LENGTH),)

        # therefore, all springs are the same length and have the same energy
        self.spring_energies.fill(interactions.calc_spring_energy(0, config.SPRING_START_LENGTH))

        # initialize particle interaction energy
        for ref_chain_idx in range(config.NUM_CHAINS):
            for ref_particle_idx in range(config.CHAIN_LEN):
                # Calculate interaction energy between this particle and all others
                ref_particle_position = self.particle_positions[ref_chain_idx, ref_particle_idx]
                interaction_energy = interactions.calc_particle_interactions(
                    self.particle_positions,
                    self.particle_types,
                    ref_chain_idx,
                    ref_particle_idx,
                    ref_particle_position
                )
                self.particle_energies[ref_chain_idx, ref_particle_idx] = interaction_energy

        """calculate total energy"""
        #IMPT: Sum of all particle energy must be divided by 2 to avoid double counting
        self.total_energy = np.sum(self.spring_energies) + np.sum(self.surface_energies) + (np.sum(self.particle_energies) / 2)
        
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
        self.particle_types[:] = target_pattern
    
    def test_move(self, ref_chain_idx, ref_particle_idx, move_dir, move_magnitude):
        
        # get new suggested co-ordinates.
        new_pos = self.particle_positions[ref_chain_idx, ref_particle_idx].copy()
        new_pos[move_dir] += move_magnitude

        # initialise a bool to indicate if the reference particle is the last particle in the chain. (avoids checking again later)
        # if the reference particle index (0 indexed) is equal to the chain length - 1 (1 indexed) then the reference particle is the last particle in the chain.
        is_last = (ref_particle_idx == config.CHAIN_LEN - 1)

        old_spring_above = 0 if is_last else self.spring_energies[ref_chain_idx, ref_particle_idx + 1]
        old_spring_below = self.spring_energies[ref_chain_idx,ref_particle_idx]
        old_surface = self.surface_energies[ref_chain_idx,ref_particle_idx]
        old_interaction = self.particle_energies[ref_chain_idx,ref_particle_idx]

        new_spring_above = 0 if is_last else interactions.calc_spring_energy(new_pos, self.particle_positions[ref_chain_idx, ref_particle_idx + 1])
        new_spring_below = interactions.calc_spring_energy(new_pos,self.particle_positions[ref_chain_idx,ref_particle_idx])
        new_surface = interactions.calc_surface_energy(new_pos[2])
        new_interaction = interactions.calc_particle_interactions(self.particle_positions,self.particle_types,ref_chain_idx,ref_particle_idx, ref_particle_position=new_pos)
        
        # calculate the total delta e
        delta_e = ((new_spring_above - old_spring_above) +  # where spring_above is 0 for last particle
            (new_spring_below - old_spring_below) + 
            (new_surface - old_surface) + 
            (new_interaction - old_interaction))

        # store the calculated energies, reference particle information,
        self.pending_move = [is_last, ref_chain_idx, ref_particle_idx, new_spring_above, new_spring_below, new_surface, new_interaction, delta_e, new_pos]

        return delta_e

    def accept_move(self):
        # update class energies and positions with information in self.pending_move
        # unpack pending move information
        is_last, ref_chain_idx, ref_particle_idx, new_spring_above, new_spring_below, new_surface, new_interaction, delta_e, new_pos = self.pending_move
        
        # Update particle position
        self.particle_positions[ref_chain_idx, ref_particle_idx] = new_pos

        # Update cached energies for the moved particle
        if not is_last: self.spring_energies[ref_chain_idx, ref_particle_idx + 1] = new_spring_above
        self.spring_energies[ref_chain_idx, ref_particle_idx] = new_spring_below
        self.surface_energies[ref_chain_idx, ref_particle_idx] = new_surface
        self.particle_energies[ref_chain_idx, ref_particle_idx] = new_interaction

        # Update total system energy
        self.total_energy += delta_e

        # Clear pending move
        self.pending_move = None
        #clear self.pending_move
