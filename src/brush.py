import numpy

#define class Brush, representing:
#    1) positions of each particle in each polymer chain.
#       3D numpy array: 
#       [chain index, particle index in chain, 3d coordiantes]
#    2) grafting position of each polymer chain.
#       2D numpy array:
#       [x,y]

class Brush:
    def __init__(self, NUM_CHAINS, CHAIN_LEN, BASE_LEN):
        self.particles = numpy.zeros((NUM_CHAINS, CHAIN_LEN, 3))
        self.graft_pos = numpy.zeros(BASE_LEN)



#prototype grafting point initialisation
n_points = 100
max_x = 10
max_y = 10

x = np.random.randint(max_x, size=n_points, dtype = uint8)
y = np.random.randint(max_y, size=n_points, )

    