import os


def check_dev_origins():
    if os.getenv("ENV") == "dev":
        return ["*"]
    else:
        return []