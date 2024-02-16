from app.config.config import env

if env == "dev":
    from app.logger.dev_logger import logger
