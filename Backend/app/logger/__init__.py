from config.config import env

if env == "dev":
    from Backend.app.logger.dev_logger import logger
