import matplotlib.pyplot as plt
from . import config

def visualize_brush(brush, title="Polymer Brush Visualization"):
    """
    Create a 3D visualization of the polymer brush state.
    
    Parameters:
    brush (Brush): The brush object containing particle positions and types
    title (str): Title for the plot
    """
    # Create 3D figure
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each polymer chain
    for chain_idx in range(config.NUM_CHAINS):
        # Get positions for this chain
        chain_positions = brush.particle_positions[chain_idx]
        chain_types = brush.particle_types[chain_idx]
        
        # Get coordinates for this chain
        x = chain_positions[:, 0]
        y = chain_positions[:, 1]
        z = chain_positions[:, 2]
        
        # Plot particles based on their type
        # Type A (1) particles in blue, Type B (-1) in red
        type_a_mask = chain_types == 1
        type_b_mask = chain_types == -1
        
        if any(type_a_mask):
            ax.scatter(x[type_a_mask], y[type_a_mask], z[type_a_mask], 
                      c='blue', s=50, label='Type A' if chain_idx == 0 else "")
        if any(type_b_mask):
            ax.scatter(x[type_b_mask], y[type_b_mask], z[type_b_mask], 
                      c='red', s=50, label='Type B' if chain_idx == 0 else "")
        
        # Plot connecting lines between particles
        ax.plot(x, y, z, 'gray', alpha=0.5)
        
        # Plot grafting point
        graft_x = brush.graft_positions[chain_idx, 0]
        graft_y = brush.graft_positions[chain_idx, 1]
        ax.scatter(graft_x, graft_y, 0, 
                  c='green', marker='s', s=50,
                  label='Grafting Point' if chain_idx == 0 else "")
        
        # Connect first particle to grafting point
        ax.plot([graft_x, x[0]], 
                [graft_y, y[0]], 
                [0, z[0]], 'gray', alpha=0.5)
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    # Add legend
    ax.legend()
    
    # Set axis limits
    ax.set_xlim(0, config.BASE_LEN_X)
    ax.set_ylim(0, config.BASE_LEN_Y)
    ax.set_zlim(0, config.CHAIN_LEN + 1)
    
    # Add a grid
    ax.grid(True)
    
    # Set the viewing angle for better visualization
    ax.view_init(elev=20, azim=45)
    
    plt.show()
    return fig, ax