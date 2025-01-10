import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import brush

def visualize_brush(brush, title="Polymer Brush Visualization"):
    """
    Create a 3D visualization of the polymer brush state.
    
    Parameters:
    brush (Brush): The brush object containing particle positions
    title (str): Title for the plot
    """
    # Create 3D figure
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each polymer chain
    for chain_idx in range(brush.NUM_CHAINS):
        chain = brush.particles[chain_idx]
        
        # Get coordinates for this chain
        x = chain[:, 0]
        y = chain[:, 1]
        z = chain[:, 2]
        
        # Plot particles
        # First 5 particles (type A) in blue, last 5 (type B) in red
        ax.scatter(x[:5], y[:5], z[:5], c='blue', s=50, label='Type A' if chain_idx == 0 else "")
        ax.scatter(x[5:], y[5:], z[5:], c='red', s=50, label='Type B' if chain_idx == 0 else "")
        
        # Plot connecting lines
        ax.plot(x, y, z, 'gray', alpha=0.5)
        
        # Plot grafting point
        ax.scatter(brush.graft_pos[chain_idx, 0], 
                  brush.graft_pos[chain_idx, 1], 
                  0, c='green', marker='s', s=50,
                  label='Grafting Point' if chain_idx == 0 else "")
        
        # Connect first particle to grafting point
        ax.plot([brush.graft_pos[chain_idx, 0], x[0]], 
                [brush.graft_pos[chain_idx, 1], y[0]], 
                [0, z[0]], 'gray', alpha=0.5)
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    # Add legend
    ax.legend()
    
    # Set axis limits
    ax.set_xlim(0, brush.BASE_LEN_X)
    ax.set_ylim(0, brush.BASE_LEN_Y)
    ax.set_zlim(0, brush.CHAIN_LEN + 1)
    
    # Add a grid
    ax.grid(True)
    
    # Optional: Set the viewing angle for better visualization
    ax.view_init(elev=20, azim=45)
    
    return fig, ax


new_brush = brush.Brush()
new_brush.initialize_brush()
visualize_brush(new_brush, title="Polymer Brush Visualization")
plt.show()