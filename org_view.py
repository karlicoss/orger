#!/usr/bin/env python3
from argparse import ArgumentParser
import logging
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional

from kython import group_by_key
from kython import atomic_write
from kython.klogging import setup_logzero
from kython.org_tools import as_org_entry as as_org, link as org_link

from org_utils import OrgTree, pick_heading
# TODO tests for determinism
# TODO unused imports? maybe even ruci?..

# TODO abc???
class OrgView:
    def __init__(
            self,
            logger_tag: str,
            default_to: str,
    ) -> None:
        self.logger = logging.getLogger(logger_tag)
        self.default_to = default_to

    def make_tree(self) -> OrgTree:
        raise NotImplementedError

    def test(self) -> None:
        raise NotImplementedError

    def main(self) -> None:
        setup_logzero(self.logger, level=logging.DEBUG)

        p = ArgumentParser()
        p.add_argument('--to', default=self.default_to)
        args = p.parse_args()

        org_tree = self.make_tree()
        with atomic_write(args.to, 'w', overwrite=True) as fo:
            fo.write(org_tree.render())

            # TODO file header?..
            # TODO nicer tree generation? yieldy?
