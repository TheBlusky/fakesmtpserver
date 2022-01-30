import logging

logger = logging.getLogger("smtpserver2api.py")


def log(message):
    logger.warning(f"[smtpserver2api.py] {message}")
