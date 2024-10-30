from loguru import logger
import os

# Ensure the log directory exists
os.makedirs("log", exist_ok=True)

# Configure the logger
logger.add("log/file_{time}.log", rotation="1 day", retention="7 days", level="INFO")


# Export the logger
def get_logger():
    return logger
