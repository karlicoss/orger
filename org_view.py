#!/usr/bin/env python3
from argparse import ArgumentParser
import logging
from tempfile import TemporaryDirectory
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional

from kython import group_by_key
from kython import atomic_write
from kython.klogging import setup_logzero
from kython.org_tools import as_org_entry as as_org, link as org_link

from org_utils import OrgTree, pick_heading
# TODO tests for determinism
# TODO unused imports? maybe even ruci?..

"""
TODO
OverWriteView -- basically what we have now
appendview -- also takes json state to track
both need new file header now...
"""


# TODO abc???
class OrgView:
    def __init__(
            self,
            logger_tag: str,
            default_to: str,
            file_header: str,
    ) -> None:
        self.logger = logging.getLogger(logger_tag)
        self.default_to = default_to
        self.file_header = file_header

    def get_items(self) -> Iterable[OrgTree]:
        raise NotImplementedError

    def main(self) -> None:
        setup_logzero(self.logger, level=logging.DEBUG)

        p = ArgumentParser()
        p.add_argument('--to', default=self.default_to)
        args = p.parse_args()

        items = self.get_items()
        with atomic_write(args.to, 'w', overwrite=True) as fo:
            org_tree = OrgTree(
                self.file_header,
                list(items)
            )
            fo.write(org_tree.render())
            # TODO nicer tree generation? yieldy?
