import logging

class MOD2:
    def __init__(self) -> None:
        self.logger = logging.getLogger(f"__main__.{__name__}")

    def hallo(self, name):
        self.logger.info(f"Hallo, {name}")
        if name == name.upper():
            self.logger.error(f"{name} is spelled in upper case.")

if __name__=="__main__":
    pass