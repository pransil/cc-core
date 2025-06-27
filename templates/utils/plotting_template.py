"""Framework standard plotting utilities with automatic saving and titles.

This template provides consistent visualization patterns across all
Claude Code Automation Framework projects.
"""

import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_framework_timestamp():
    """Get timestamp in framework standard format.
    
    Framework Standard: YYYY-MM-DD-HH:mm format for all files
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime('%Y-%m-%d-%H:%M')


def setup_plot_with_title(fig, model_name: str, plot_type: str = "Training Progress"):
    """Add framework standard title to plot.
    
    Framework Standard: All plots must show model being tested
    
    Args:
        fig: Matplotlib figure object
        model_name: Name of the model being tested
        plot_type: Type of plot (e.g., "Training Progress", "Results")
    """
    title = f'{model_name} {plot_type}'
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # Adjust layout to make room for title
    plt.subplots_adjust(top=0.93)


def save_and_show_plot(fig, base_filename: str, model_name: str = "", 
                      plots_dir: str = "plots", show_plot: bool = True):
    """Save plot with timestamp and show without blocking.
    
    Framework Standard: All plots automatically saved with timestamps
    
    Args:
        fig: Matplotlib figure object
        base_filename: Base name for the file (without extension)
        model_name: Name of model (included in filename)
        plots_dir: Directory to save plots
        show_plot: Whether to display the plot
        
    Returns:
        Path to saved file
    """
    # Create plots directory
    plots_path = Path(plots_dir)
    plots_path.mkdir(exist_ok=True)
    
    # Generate timestamped filename
    timestamp = get_framework_timestamp()
    
    if model_name:
        filename = f"{model_name}_{base_filename}_{timestamp}.png"
    else:
        filename = f"{base_filename}_{timestamp}.png"
    
    plot_path = plots_path / filename
    
    # Save plot with high quality
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"📊 Plot saved: {plot_path}")
    
    if show_plot:
        # Show plot without blocking execution
        plt.show(block=False)
        plt.pause(0.1)  # Brief pause to ensure plot displays
    
    plt.close()
    return plot_path


def create_framework_plot(model_name: str, plot_type: str = "Training Progress",
                         figsize=(12, 8), save_base_name: str = "plot"):
    """Create a plot following framework standards.
    
    Framework Standard: Consistent plot setup across all projects
    
    Args:
        model_name: Name of model being visualized
        plot_type: Type of plot for title
        figsize: Figure size
        save_base_name: Base name for saved file
        
    Returns:
        Figure and axes objects
    """
    fig, axes = plt.subplots(figsize=figsize)
    setup_plot_with_title(fig, model_name, plot_type)
    
    # Store save info for later use
    fig._framework_save_base = save_base_name
    fig._framework_model_name = model_name
    
    return fig, axes


def finalize_framework_plot(fig, show_plot: bool = True):
    """Finalize and save framework plot.
    
    Framework Standard: Standard plot finalization
    
    Args:
        fig: Matplotlib figure object
        show_plot: Whether to display the plot
    """
    plt.tight_layout()
    
    # Use stored save info
    base_name = getattr(fig, '_framework_save_base', 'plot')
    model_name = getattr(fig, '_framework_model_name', '')
    
    save_and_show_plot(fig, base_name, model_name, show_plot=show_plot)


# Framework Integration Example:
# 
# from utils.plotting_template import create_framework_plot, finalize_framework_plot
# 
# # Create plot with framework standards
# fig, (ax1, ax2) = create_framework_plot("CNN_Deep", "Training Results", save_base_name="training_curves")
# 
# # Add your plot content
# ax1.plot(epochs, loss, label='Training Loss')
# ax1.set_title('Loss Curves')
# ax1.legend()
# 
# ax2.plot(epochs, accuracy, label='Accuracy')
# ax2.set_title('Accuracy Curves')
# ax2.legend()
# 
# # Finalize with framework standards
# finalize_framework_plot(fig)