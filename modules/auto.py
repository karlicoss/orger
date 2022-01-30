#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading, error

from typing import Optional, List
from datetime import datetime

from more_itertools import bucket

from my.core.common import asdict
from pprint import pformat
def pp_item(i, **kwargs) -> str:
    # annoying, ppring doesn't have dataclass support till 3.10 https://bugs.python.org/issue43080
    return pformat(asdict(i), **kwargs)


class Auto(Mirror):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO move this functionality to base module? might be useful for all modules
        self.extra_warnings: List[str] = []


    def get_items(self) -> Mirror.Results:
        args = self.cmdline_args; assert args is not None
        return self.auto(
            it=args.name,
            group_by=args.group_by,
        )


    # TODO hmm maybe reuse HPI core.query.select?
    # could abuse that for grouping by, sorting, raising errors, filtering fields, etc
    def auto(self, it, *, group_by: Optional[str]=None) -> Mirror.Results:


        if isinstance(it, str):
            # treat as HPI query target
            from my.core.__main__ import _locate_functions_or_prompt
            [it] = _locate_functions_or_prompt([it], prompt=False)

        if group_by is None:
            for i in it():
                if isinstance(i, Exception):
                    yield error(i)
                else:
                    yield self.render_one(i)
        else:
            good = []
            for i in it():
                if isinstance(i, Exception):
                    yield error(i)
                    continue
                good.append(i)

            _group_by = group_by  # make mypy happy
            groups = bucket(good, key=lambda i: getattr(i, _group_by))
            for key in groups:
                group = list(groups[key])

                def chit():
                    for i in group:
                        yield self.render_one(i)
                children = list(chit())

                yield node(
                    heading=f'{group_by}: {key}',
                    children=children,
                )
        if len(self.extra_warnings) > 0:
            self.file_header = self.file_header + '\n'.join('# ' + w for w in ['', *self.extra_warnings]) + '\n'


    def _warn(self, w: str):
        if w not in self.extra_warnings:
            self.extra_warnings.append(w)


    def render_one(self, i) -> node:
        self._warn('WARNING: Default renderer is used! Implement render_one if you want nicer rendering')

        d = asdict(i)

        datetimes = [(k, v) for k, v in d.items() if isinstance(v, datetime)]
        dt: Optional[datetime] = None
        if len(datetimes) == 1:
            [(k, dt)] = datetimes
            # todo maybe warn that datetime is guessed
            del d[k] # probs no need to press twice?
            self._warn(f"NOTE: {i.__class__} is using '{k}' as the timestamp")
        else:
            self._warn(f"WARNING: {i.__class__} couldn't guess timestamp: expected single datetime field, got {datetimes}")

        return node(
            # todo could extract ids here?
            heading=dt_heading(dt, str(i.__class__)),
            body=Quoted(pp_item(d, width=120)),
        )


def setup_parser(p) -> None:
    p.add_argument(
        '--name',
        type=str,
        required=True,
        help="HPI function name (see 'hpi query --help')",
    )
    p.add_argument(
        '--group-by',
        type=str,
        default=None,
        help='key to group items by',
    )


if __name__ == '__main__':
    Auto.main(setup_parser=setup_parser)
