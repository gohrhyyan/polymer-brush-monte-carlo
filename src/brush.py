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
        self.CHAIN_LEN = CHAIN_LEN  # Length of each polymer chain
        self.BASE_LEN_X = BASE_LEN_X  # Number of grid points in the X direction
        self.BASE_LEN_Y = BASE_LEN_Y  # Number of grid points in the Y direction
        
        # Initialize a 3D array to store particle positions for each chain
        # Shape: (NUM_CHAINS, CHAIN_LEN, 3) for x, y, z positions
        self.particles = np.zeros((NUM_CHAINS, CHAIN_LEN, 3))
        
        # Initialize an array to store graft positions for each chain
        # Shape: (NUM_CHAINS, 2) for x and y coordinates
        self.graft_pos = np.zeros((NUM_CHAINS, 2))
        
    def initialize_graft_points(self):
        # Create a 2D grid of points with x-coordinates and y-coordinates
        # `x` and `y` are 2D arrays representing all x and y values in the grid
        x, y = np.meshgrid(np.arange(self.BASE_LEN_X), np.arange(self.BASE_LEN_Y))
        
        # Flatten the grid into a list of all possible points
        # Each point is represented as (x, y) in the grid
        possible_points = np.column_stack((x.ravel(), y.ravel()))
        
        # Randomly select NUM_CHAINS unique points from the possible points
        # `replace=False` ensures no duplicate points are selected
        indices = np.random.choice(len(possible_points), self.NUM_CHAINS, replace=False)
        
        # Use the selected indices to choose graft points from the grid
        self.graft_pos = possible_points[indices]
        
        # Print the selected graft positions for debugging
        print(self.graft_pos)

# Create an instance of the Brush class with default parameters
brush = Brush()

# Initialize and print randomly selected graft points
brush.initialize_graft_points()











    