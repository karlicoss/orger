#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading, error

from datetime import datetime
from typing import Optional, List, Iterator, Any
from pprint import pformat
import string

from more_itertools import bucket

from my.core.common import asdict


def pp_item(i, **kwargs) -> str:
    # annoying, pprint doesn't have dataclass support till 3.10 https://bugs.python.org/issue43080
    return pformat(asdict(i), **kwargs)


class Auto(Mirror):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO move this functionality to base module? might be useful for all modules
        self.extra_warnings: List[str] = []

        # these will be set below
        self.group_by_attr: Optional[str] = None
        self.body_attr    : Optional[str] = None
        self.title_attr   : Optional[str] = None


    def get_items(self) -> Mirror.Results:
        args = self.cmdline_args; assert args is not None
        self.group_by_attr = args.group_by
        self.body_attr     = args.body
        self.title_attr    = args.title
        return self.auto(it=args.name)


    # TODO hmm maybe reuse HPI core.query.select?
    # could abuse that for grouping by, sorting, raising errors, filtering fields, etc
    def auto(self, it) -> Mirror.Results:
        group_by = self.group_by_attr
        if isinstance(it, str):
            # treat as HPI query target
            from my.core.__main__ import _locate_functions_or_prompt
            [it] = _locate_functions_or_prompt([it], prompt=False)

        if group_by is None:
            for i in it():
                if isinstance(i, Exception):
                    yield error(i)
                else:
                    yield from self.render_one(i)
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
                        yield from self.render_one(i)
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


    def render_one(self, thing) -> Iterator[node]:
        self._warn('WARNING: Default renderer is used! Implement render_one if you want nicer rendering')

        thing_dict = asdict(thing)
        cls = thing.__class__

        datetimes = [(k, v) for k, v in thing_dict.items() if isinstance(v, datetime)]
        dt: Optional[datetime] = None
        if len(datetimes) == 1:
            [(k, dt)] = datetimes
            # todo maybe warn that datetime is guessed
            del thing_dict[k]  # probs no need to press twice?
            self._warn(f"NOTE: {cls} is using '{k}' as the timestamp")
        else:
            self._warn(f"WARNING: {cls} couldn't guess timestamp: expected single datetime field, got {datetimes}")

        # todo could pass fmt string for group as well?
        if self.group_by_attr is not None:
            try:
                thing_dict.pop(self.group_by_attr)
            except KeyError as e:
                yield error(e)

        def fmt_attr(attr: Optional[str]) -> Optional[str]:
            if attr is None:
                return None

            fake_self: Any = object()  # fine to call it as class method here..
            fields = [
                f
                for (_, f, _, _) in string.Formatter.parse(fake_self, attr)
                if f is not None  # might be none for the last bit (before the static bit)
            ]
            fstr: str
            if len(fields) == 0:
                # must be field name without formatting string?
                # TODO maybe deprecate this.. it's not a huge deal to pass extra curlies
                fields = [attr]
                fstr = '{' + attr + '}'
            else:
                fstr = attr

            # here we can't use the thing_dict since formatter string might refer to properties
            # TODO maybe use freezer instead?... or dump to dict with properties
            res = fstr.format(**{f: getattr(thing, f) for f in fields})
            for f in fields:
                thing_dict.pop(f, None)  # might not exist if it was a @property
            return res


        title = fmt_attr(self.title_attr)
        body  = fmt_attr(self.body_attr)

        node_title = cls.__name__ if title is None else title
        node_body = Quoted(pp_item(thing_dict, width=120)).quoted()
        if body is not None:
            node_body += '\n' + body

        yield node(
            heading=dt_heading(dt, node_title),
            body=node_body,
        )


def setup_parser(p) -> None:
    p.add_argument(
        '--name',
        type=str,
        required=True,
        help="HPI function name (see 'hpi query --help')",
    )
    p.add_argument('--group-by', type=str, default=None, help='field to group items by')
    p.add_argument('--body'    , type=str, default=None, help='field to use as item body')
    p.add_argument('--title'   , type=str, default=None, help='field to use as item title')
    # will support later
    # p.add_argument('--id'      , type=str, default=None, help='field to use as item ID')


if __name__ == '__main__':
    Auto.main(setup_parser=setup_parser)
