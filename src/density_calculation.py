#Flatten and filter out elements with z < 2
def calcdensity(new_brush):
    filtered_positions = [
        particle.tolist()
        for row in new_brush.particle_positions
        for particle in row
        if particle[2] <= 2
    ]

    density = len(filtered_positions)/200

    return density
