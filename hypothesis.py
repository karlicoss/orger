#!/usr/bin/env python3
from argparse import ArgumentParser
import logging
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional

from my.hypothesis import get_pages # type: ignore

from kython import group_by_key
from kython import atomic_write
from kython.klogging import setup_logzero
from kython.org_tools import as_org_entry as as_org, link as org_link


def get_logger():
    return logging.getLogger('hypothesis-view')

import sys, ipdb, traceback; exec("def info(type, value, tb):\n    traceback.print_exception(type, value, tb)\n    ipdb.pm()"); sys.excepthook = info # type: ignore
def main():
    # TODO need to group by source??
    for p in get_pages():
        print(p)

if __name__ == '__main__':
    main()
