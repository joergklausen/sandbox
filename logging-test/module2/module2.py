import logging

class MOD2:
    def __init__(self, main_logger: str) -> None:
        self.logger = logging.getLogger(f"{main_logger}.{__name__}")

    def hallo(self, name):
        self.logger.info(f"Hallo, {name}")
        if name == name.upper():
            self.logger.warning(f"{name} is spelled in upper case.")

if __name__=="__main__":
    pass