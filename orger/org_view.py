#!/usr/bin/env python3
import argparse
from argparse import ArgumentParser, Namespace
import logging
import inspect
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
from typing import List, Tuple, Iterable, Optional

# TODO dekythonize
from kython.state import JsonState

from .inorganic import OrgNode
from .common import PathIsh, atomic_append_check, assert_not_edited, setup_logger

# TODO tests for determinism? not sure where should they be...
# think of some generic thing to test that?

Key = str
OrgWithKey = Tuple[Key, OrgNode]

class OrgView:
    """
    Override to get autogenerated header
    """
    # TODO remove file attribute
    file: Optional[str] = None

    logger_tag: Optional[str] = None

    def __init__(
            self,
            cmdline_args: Optional[Namespace]=None,
            file_header: Optional[str]=None,
    ) -> None:
        self.cmdline_args = cmdline_args
        tag = self.name() if self.logger_tag is None else self.logger_tag
        self.logger = logging.getLogger(tag)

        tool = Path(inspect.getfile(self.__class__)).absolute()
        self.file_header = file_header if file_header is not None else f"# AUTOGENERATED BY {tool}\n"

    @classmethod
    def name(cls):
        return cls.__name__

    def get_items(self) -> Iterable[OrgWithKey]:
        raise NotImplementedError

    def main_common(self) -> None:
        setup_logger(self.logger, level=logging.DEBUG)


# TODO wonder if I could reuse append bits here?
class OrgViewOverwrite(OrgView):
    @classmethod
    def main(cls, default_to=None, setup_parser=None) -> None:
        p = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('--to', type=Path, default=Path(cls.name() + '.org'))
        if setup_parser is not None:
            setup_parser(p)

        args = p.parse_args()
        inst = cls(cmdline_args=args)
        inst._run(to=args.to)


    def _run(self, to: Path):
        self.main_common()

        # TODO make it read only??
        org_tree = self.make_tree()
        rtree = org_tree.render()

        assert_not_edited(to)
        # again, not properly atomic, but hopefully enough
        # TODO create a github issue, maybe someone comes up with proper way of solving this
        to.touch()
        check_call(['chmod', '+w', to])
        to.write_text(rtree)
        check_call(['chmod', '-w', to])


    def make_tree(self) -> OrgNode:
        # TODO shit; hacky...
        items = [p[1] for p in self.get_items()] # we don't need keys here
        split = self.file_header.splitlines()
        # TODO quite hacky..
        heading = split[0]
        body = '\n'.join(split[1:])
        return OrgNode(
            # TODO shit. are newlines sanitized from file header??
            heading=heading,
            body=body,
            children=items,
        )


class OrgViewAppend(OrgView):
    def _run(
            self,
            to: Path,
            state_path: Path,
            init: bool=False,
            dry_run: bool=False,
    ) -> None:
        state = JsonState(
            path=state_path,
            logger=self.logger,
            dry_run=dry_run,
        )
        items = list(self.get_items())

        from collections import Counter
        dups = [k for k, cnt in Counter(i[0] for i in items).items() if cnt > 1]
        if len(dups) > 0:
            raise RuntimeError(f'Duplicate items {dups}')

        if not to.exists():
            if init:
                self.logger.warning("target %s didn't exist, initializing!", to)
                atomic_append_check(to, self.file_header + '\n')
            else:
                raise RuntimeError(f"target {to} doesn't exist! Try running with --init")

        for key, item in items:
            def action(item=item):
                # not sure about this newline, but better to have extra whitespace than rely on trailing
                rendered = '\n' + item.render(level=1)
                atomic_append_check(
                    to,
                    rendered,
                )
            self.logger.debug('processing %s', key)
            state.feed(
                key=key,
                value=item, # TODO not sure about this one... perhaps only link?
                action=action,
            )

    @classmethod
    def main(cls, default_to=None, default_state=None) -> None:
        p = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        p.add_argument('--to'   , type=Path, default=Path(cls.name() + '.org')       , help='file where new items are appended')
        p.add_argument('--state', type=Path, default=Path(cls.name() + '.state.json'), help='state file for keeping track of handled items')
        p.add_argument('--init', action='store_true')
        p.add_argument('--dry-run', action='store_true')
        args = p.parse_args()

        inst = cls(cmdline_args=args)
        inst.main_common()
        inst._run(
            to=args.to,
            state_path=args.state,
            init=args.init,
            dry_run=args.dry_run,
        )


def test_org_view_overwrite(tmp_path: Path):
    class TestView(OrgViewOverwrite):
        def __init__(self, items: List[OrgWithKey], *args, **kwargs) -> None:
            super().__init__(*args, file_header='# autogenerated!\n', **kwargs) # type: ignore
            self.items = items

        def get_items(self):
            return self.items

    rpath = tmp_path / 'test.org'

    TestView([])._run(to=rpath)
    assert rpath.read_text() == '# autogenerated!\n'

    TestView([
        # TODO shit, it's gonna use implicit date??
        ('first' , OrgNode(heading='whatever')),
        ('second', OrgNode(heading='alala')), # TODO why was that even necessary??
    ])._run(to=rpath)
    # TODO eh, perhaps use trailing space?
    assert rpath.read_text() == """
# autogenerated!

* whatever
* alala""".lstrip()


# TODO major bit of this test really belongs to json state..
# TODO try with error, make sure it's executed before action
def test_org_view_append(tmp_path: Path):
    import json
    class TestView(OrgViewAppend):
        def __init__(self, items: List[OrgWithKey], *args, **kwargs) -> None:
            super().__init__(*args, file_header='# autogenerated!', **kwargs) # type: ignore
            self.items = items

        def get_items(self):
            for i in self.items:
                yield i

    rpath = tmp_path / 'res.org'
    spath = tmp_path / 'state.json'

    def run_view(items, **kwargs):
        TestView(items)._run(
            to=rpath,
            state_path=spath,
            **kwargs,
        )

    def get_state():
        return set(json.loads(spath.read_text()).keys())

    items = []
    run_view([], init=True)
    assert rpath.read_text() == """
# autogenerated!
""".lstrip()
    # TODO do we need to touch state too??

    items.append(
        ('first', OrgNode(heading='i am first')),
    )
    run_view(items)
    assert rpath.read_text() == """
# autogenerated!

* i am first""".lstrip()
    assert get_state() == {'first'}


    items.append(
        ('second', OrgNode('i am second')),
    )
    run_view(items)
    assert rpath.read_text() == """
# autogenerated!

* i am first
* i am second""".lstrip()
    assert get_state() == {'first', 'second'}


    rpath_time = rpath.stat().st_mtime
    spath_time = rpath.stat().st_mtime
    run_view(items)
    assert rpath.stat().st_mtime == rpath_time
    assert spath.stat().st_mtime == spath_time

