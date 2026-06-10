import logging
import json
import sys
from datetime import datetime


class JSONFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logging(level: str = "INFO"):
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logger.handlers = [handler]
