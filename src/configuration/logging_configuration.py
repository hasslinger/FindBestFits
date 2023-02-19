# Import the default logging module
import logging

log = logging.getLogger('FindBestFitsLogger')
# Set a log level for the logger
log.setLevel(logging.INFO)
# Create a console handler
handler = logging.StreamHandler()
# Set INFO level for handler
handler.setLevel(logging.INFO)
# Create a message format that matches earlier example
formatter = logging.Formatter('[%(levelname)s - %(filename)s: %(funcName)s]:   %(message)s')
# Add our format to our handler
handler.setFormatter(formatter)
# Add our handler to our logger
log.addHandler(handler)
