"""
Logging configuration for the trading bot
Provides colored console output and file logging
"""

import logging
import colorlog
from datetime import datetime
import os


def setup_logger(name: str = "TradingBot", level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with both console and file handlers
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    logger = colorlog.getLogger(name)
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console Handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(numeric_level)
    
    console_format = colorlog.ColoredFormatter(
        "%(log_color)s┃ %(asctime)s ┃ %(name)-15s ┃ %(levelname)-8s ┃ %(message)s%(reset)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'light_green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File Handler
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = os.path.join(
        log_dir,
        f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(numeric_level)
    
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    logger.propagate = False
    
    return logger
