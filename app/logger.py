import logging
from datetime import UTC, datetime

import yaml
from pythonjsonlogger import jsonlogger

from app.config import settings

with open("./logging.conf.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("logger")
jsonLogger = logging.getLogger()


streamHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

streamHandler.setFormatter(formatter)
jsonLogger.addHandler(streamHandler)

jsonLogger.setLevel(settings.logging.LOG_LEVEL)

if settings.project.MODE == "TEST":
    logger.setLevel("ERROR")
    jsonLogger.setLevel("ERROR")
