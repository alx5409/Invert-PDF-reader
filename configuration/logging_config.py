import logging
import os

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO, # Info level to log general information, also shows errors
    format='%(asctime)s - %(levelname)s - %(message)s'
)