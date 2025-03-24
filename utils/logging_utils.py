import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from datetime import datetime

def setup_logger(logger_name, log_filename, max_bytes=51200, backup_count=100):
    """
    Set up a logger with a concurrent rotating file handler.
    Args:
        logger_name (str): Name of the logger.
        log_filename (str): Path to the log file.
        max_bytes (int): Maximum size of the log file before rotation.
        backup_count (int): Number of backup log files to keep.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    
    # Avoid adding multiple handlers if the logger already exists
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create a concurrent rotating file handler
        handler = ConcurrentRotatingFileHandler(
            log_filename, 
            mode='a', 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        handler.addFilter(logging.Filter(name=logger_name))  # Filter logs by logger name

        # Add the handler to the logger
        logger.addHandler(handler)

    return logger

def ensure_folder_exists(path):
    """
    Ensure that the specified folder exists. If not, create it.
    Args:
        path (str): Path to the folder.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")
    else:
        print(f"Folder already exists: {path}")

# Get the current date in the format YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')

# Define the paths for app_event and sys_event logs
app_event_folder = 'data/logs/events/app_event'
sys_event_folder = 'data/logs/events/sys_event'

# Ensure the folders exist
ensure_folder_exists(app_event_folder)
ensure_folder_exists(sys_event_folder)

# Set up logger for app_event with maxBytes limit and backupCount
app_event_log_filename = os.path.join(app_event_folder, f'app_events_{current_date}.out')
app_event = setup_logger('app_event', app_event_log_filename, max_bytes=51200, backup_count=100)

# Set up logger for sys_event with maxBytes limit and backupCount
sys_event_log_filename = os.path.join(sys_event_folder, f'sys_event_{current_date}.out')
sys_event = setup_logger('sys_event', sys_event_log_filename, max_bytes=51200, backup_count=100)
