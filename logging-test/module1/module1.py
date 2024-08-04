import logging

class MOD1:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def hallo(self, name):
        self.logger.info(f"Hallo, {name}")

if __name__=="__main__":
    pass