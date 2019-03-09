#!/usr/bin/env python3
import logging

from kython.klogging import setup_logzero

def get_logger():
    return logger.getLogger('instapaper-org-view')

def main():
    logger = get_logger()
    setup_logzero(logger, level=logging.DEBUG)
    pass

if __name__ == '__main__':
    main()
