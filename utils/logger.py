"""
Logging yapılandırması
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Logger kurulumu"""
    
    # Logger oluştur
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Eğer handler zaten eklenmişse tekrar ekleme
    if logger.handlers:
        return logger
    
    # Formatter oluştur
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (logs klasörü oluştur)
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(
        logs_dir / f"product_analyzer_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Logger al"""
    return logging.getLogger(name)
