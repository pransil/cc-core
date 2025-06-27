"""Framework standard notification utilities for user interaction.

This template provides consistent user interaction patterns across all
Claude Code Automation Framework projects.
"""

import os
import sys


def ring_bell(count=1):
    """Ring system bell for audio notification.
    
    Framework Standard: Use for all user interactions
    
    Args:
        count: Number of bells to ring (1 for input, 3 for warnings)
    """
    bell_string = '\a' * count
    os.system(f"echo -e '{bell_string}'")


def prompt_with_bell(message):
    """Prompt user for input with bell notification.
    
    Framework Standard: Use for all user input requests
    
    Args:
        message: The prompt message to display
        
    Returns:
        User's input response
    """
    ring_bell(1)
    return input(message)


def data_fallback_warning(reason, fallback_type="synthetic data"):
    """Show clear warning when real data can't be used.
    
    Framework Standard: Required for all data fallback scenarios
    
    Args:
        reason: Reason why real data isn't available
        fallback_type: Type of fallback being offered
        
    Returns:
        True if user approves fallback, False otherwise
    """
    print(f"⚠️  REAL DATA NOT AVAILABLE: {reason}")
    print("🔔🔔🔔 DATA FALLBACK WARNING!")
    ring_bell(3)
    
    response = prompt_with_bell(f"Real data unavailable. Use {fallback_type} instead? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Stopping execution as requested.")
        return False
    
    return True


def confirm_action(message):
    """Ask for user confirmation with bell.
    
    Framework Standard: Use for all confirmation dialogs
    
    Args:
        message: Confirmation message
        
    Returns:
        True if user confirms, False otherwise
    """
    response = prompt_with_bell(f"{message} (y/n): ")
    return response.lower() == 'y'


def notify_file_saved(file_path, file_type="File"):
    """Standard notification for file saves.
    
    Framework Standard: Use for all file save operations
    
    Args:
        file_path: Path to saved file
        file_type: Type of file (e.g., "Plot", "Results", "Model")
    """
    print(f"📄 {file_type} saved: {file_path}")


# Framework Integration Example:
# 
# from utils.notifications import data_fallback_warning, prompt_with_bell, notify_file_saved
# 
# # Data fallback protection
# if not real_data_available:
#     if not data_fallback_warning("Real dataset not found"):
#         return
# 
# # User input with audio
# model_name = prompt_with_bell("Enter model name: ")
# 
# # File save notification
# notify_file_saved(results_file, "Training Results")