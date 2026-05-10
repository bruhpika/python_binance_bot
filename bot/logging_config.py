import logging
from logging.handlers import RotatingFileHandler
import os

_configured = False

def get_logger(name: str, log_file: str = "logs/trading_bot.log") -> logging.Logger:
    """Configures and returns a logger instance with file and stream handlers."""
    global _configured
    logger = logging.getLogger(name)
    
    # Configure the root logger once
    if not _configured:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(module)s | %(message)s")
        
        fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        
        # Guard against duplicate handlers on root
        if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
            root_logger.addHandler(fh)
        if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
            root_logger.addHandler(ch)
            
        _configured = True
        
    return logger
