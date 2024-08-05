# https://docs.python.org/3/howto/logging-cookbook.html#using-logging-in-multiple-modules

import logging

from module1.module1 import MOD1
from module2.module2 import MOD2

def main():
    logger_main = __name__
    logger = logging.getLogger(logger_main)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs warning and above messages
    fh = logging.FileHandler(f"{logger_main}.log")
    fh.setLevel(logging.WARNING)

    # create console handler which logs even debugging information
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s: %(levelname)s from %(name)s: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('creating an instance of MOD1')
    mod1 = MOD1(logger_main)
    logger.info('created an instance of MOD1')
    logger.info('calling MOD1.hallo("John")')
    mod1.hallo("John")
    logger.info('finished MOD1.hallo("John")')
    logger.info('creating an instance of MOD2')
    mod2 = MOD2()
    logger.info('created an instance of MOD2')
    logger.info('calling MOD2.hallo("Mia")')
    mod2.hallo("Mia")
    logger.info('finished MOD2.hallo("Mia")')
    logger.info('calling MOD2.hallo("DAVID")')
    mod2.hallo("DAVID")
    logger.info('finished MOD2.hallo("DAVID")')

if __name__=="__main__":
    main()