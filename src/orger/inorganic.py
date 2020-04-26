from datetime import datetime, date
import logging
from pathlib import Path
import re
import os
from collections import OrderedDict
from typing import NamedTuple, Optional, Sequence, Dict, Mapping, Any, Tuple, TypeVar, Callable, Union, List

Dateish = Union[datetime, date]

def link(*, url: str, title: Optional[str]) -> str:
    """
    >>> link(url='http://reddit.com', title='[R]eddit!')
    '[[http://reddit.com][Reddit!]]'
    """
    url = _sanitize_heading(url)
    if title == '':
        # org mode doesn't like empty titles..
        # TODO sanitize_title?
        title = None
    if title is not None:
        title = _sanitize_heading(title)
        return f'[[{url}][{title}]]'
    else:
        return f'[[{url}]]'


def timestamp(t: Dateish, inactive: bool=False, active: bool=False) -> str:
    """
    >>> dt = datetime.strptime('19920110 04:45', '%Y%m%d %H:%M')
    >>> timestamp(dt)
    '1992-01-10 Fri 04:45'
    """
    beg, end = '', ''
    if inactive:
        beg, end = '[]'
    if active:
        beg, end = '<>'
    r = asorgdate(t)
    if isinstance(t, datetime):
        r += " " + asorgtime(t)
    return beg + r + end


# TODO priority
# TODO for sanitizing, have two strategies: error and replace?
def asorgoutline(
        heading: Optional[str] = None,
        todo: Optional[str] = None,
        tags: Sequence[str] = [],
        scheduled: Optional[Dateish] = None,
        # TODO perhaps allow list of tuples? properties might be repeating
        properties: Optional[Mapping[str, str]]=None,
        body: Optional[str] = None,
        level: int=1,
) -> str:
    r"""
    Renders Org mode outline (apart from children)

    >>> asorgoutline(
    ...     heading=None,
    ...     tags=['hi'],
    ...     body='whatever...'
    ... )
    '* :hi:\n whatever...'
    >>> asorgoutline(heading=None, todo=None, tags=(), level=2)
    '** '
    >>> asorgoutline(heading='heading', body=None)
    '* heading'
    >>> asorgoutline(heading='heading', body='keep\n newlines\n')
    '* heading\n keep\n  newlines\n'
    >>> asorgoutline(heading='123', todo='TODO', level=0)
    'TODO 123'
    >>> asorgoutline(heading='*abacaba', body='***whoops', tags=('baa@d tag', 'goodtag'))
    '* *abacaba :baa@d_tag:goodtag:\n ***whoops'
    >>> asorgoutline(heading='just heading', level=0)
    'just heading'
    >>> asorgoutline(heading='', level=0)
    ''
    >>> asorgoutline(heading='task', body='hello', scheduled=datetime.utcfromtimestamp(0))
    '* task\nSCHEDULED: <1970-01-01 Thu 00:00>\n hello'
    """
    if heading is None:
        heading = ''
    heading = re.sub(r'\s', ' ', heading)

    # TODO not great that we always pad body I guess. maybe needs some sort of raw_body argument?
    if body is not None:
        body = _sanitize_body(body)

    parts = []

    if level > 0:
        parts.append('*' * level)

    if todo is not None:
        parts.append(todo)

    if len(heading) > 0:
        parts.append(heading)

    if len(tags) > 0:
        # tags_s = ('' if heading.endswith(' ') else ' ') +
        tags_s = ':' + ':'.join(map(_sanitize_tag, tags)) + ':'
        parts.append(tags_s)

    sch_lines = [] if scheduled is None else [
        'SCHEDULED: ' + timestamp(scheduled, active=True)
    ]

    props_lines: List[str] = []
    props = {} if properties is None else properties
    if len(props) > 0:
        props_lines.append(':PROPERTIES:')
        props_lines.extend(f':{prop}: {value}' for prop, value in props.items())
        props_lines.append(':END:')

    body_lines = [] if body is None else [body]

    if level > 0 and len(parts) == 1:
        # means it's only got level stars, so we need to make sure space is present (otherwise it's not an outline)
        parts.append('')
    lines = [
        ' '.join(parts), # TODO just in case check that parts doesn't have newlines?
        *sch_lines,
        *props_lines,
        *body_lines,
    ]
    # TODO careful here, I guess actually need some tests for endlines
    return '\n'.join(lines)


T = TypeVar('T')
Lazy = Union[T, Callable[[], T]]


class OrgNode(NamedTuple):
    """
    Meant to be somewhat compatible with https://orgparse.readthedocs.io/en/latest/#orgparse.node.OrgNode
    """
    heading: Lazy[str]
    todo: Optional[str] = None
    tags: Sequence[str] = ()
    scheduled: Optional[Dateish] = None
    properties: Optional[Mapping[str, str]] = None
    # TODO make body lazy as well?
    body: Optional[str] = None
    children: Sequence[Any] = () # mypy wouldn't allow recursive type here...

    def _render_self(self) -> str:
        return asorgoutline(
            heading=_from_lazy(self.heading),
            todo=self.todo,
            tags=self.tags,
            properties=self.properties,
            scheduled=self.scheduled,
            body=self.body,
            level=0,
        )

    def _render_hier(self) -> List[Tuple[int, str]]:
        res = [(0, self._render_self())]
        for ch in self.children:
            # TODO make sure there is a space??
            # TODO shit, would be nice to tabulate?.. not sure
            res.extend((l + 1, x) for l, x in ch._render_hier())
        return res

    def render(self, level: int=1) -> str:
        r"""
        >>> OrgNode('something', todo='TODO').render()
        '* TODO something'
        >>> OrgNode('something else').render()
        '* something else'
        >>> OrgNode(heading=lambda: 'hi', body='so lazy...').render()
        '* hi\n so lazy...'
        >>> OrgNode('#+FILETAGS: sometag', children=[OrgNode('subitem')]).render(level=0)
        '#+FILETAGS: sometag\n* subitem'
        """
        rh = self._render_hier()
        rh = [(level + l, x) for l, x in rh]
        return '\n'.join('*' * l + (' ' if l > 0 else '') + x for l, x in rh)

node = OrgNode


## helper functions

def asorgdate(t: Dateish) -> str:
    return t.strftime("%Y-%m-%d %a")


def asorgtime(t: datetime) -> str:
    return t.strftime("%H:%M")


# meh
def _from_lazy(x: Lazy[T]) -> T:
    if callable(x):
        return x()
    else:
        return x


def _sanitize_heading(x: str) -> str:
    # TODO do something smarter? e.g. https://stackoverflow.com/questions/12737564/escaping-characters-in-emacs-org-mode
    return re.sub(r'[\]\[]', '', x)


# TODO allow passing raw body?
def _sanitize_body(text: str) -> str:
    r"""
    >>> _sanitize_body('this is not a heading!:\n* hi')
    ' this is not a heading!:\n * hi'
    >>> _sanitize_body('Some thoughts:\r\n\r\n* convenience')
    ' Some thoughts:\n \n * convenience'
    """
    # TODO hmm. maybe just tabulating with 1 space is enough?...
    text = text.replace('\r\n', os.linesep)
    return ''.join(' ' + l for l in text.splitlines(keepends=True))


def _sanitize_tag(tag: str) -> str:
    """
    >>> _sanitize_tag('test-d@shes')
    'test_d@shes'
    """
    # https://orgmode.org/manual/Tags.html
    # Tags are normal words containing letters, numbers, ‘_’, and ‘@’.
    # TODO not sure, perhaps we want strict mode for formatting?
    # TODO reuse orgparse regexes?
    return re.sub(r'[^@\w]', '_', tag)

