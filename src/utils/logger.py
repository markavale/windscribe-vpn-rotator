import logging
import os
from datetime import datetime

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with only a console handler."""
        self.logger = logging.getLogger('windscribe_vpn')
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatters and add it to the handler
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        
        # Add the handler to the logger
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the logger instance."""
        return self.logger 