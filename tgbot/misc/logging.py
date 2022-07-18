from loguru import logger


def setup():
    logger.add("logs/tiktoklaodrobot.log", rotation="00:00", level="DEBUG")
