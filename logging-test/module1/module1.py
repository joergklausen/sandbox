import logging

class MOD1:
    def __init__(self, logger_main: str) -> None:
        self.logger = logging.getLogger(f"{logger_main}.{__name__}")

    def hallo(self, name):
        self.logger.info(f"Hallo, {name}")

if __name__=="__main__":
    pass