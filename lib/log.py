"""
Provide a module logger
"""
import logging

formatter = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('StarFollowerLog')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
