#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading, error
from orger import pandoc

import my.github.all as github
# todo use later: import my.github.ghexport as gh. also careful about using events() -- need to sort?
# I guess makes sense to generally expose get_ methods?


class Github(Mirror):
    def get_items(self) -> Mirror.Results:
        # TODO just use events? but need to sort first..
        for e in github.get_events():
            if isinstance(e, Exception):
                yield error(e)
                continue
            # TODO filter only events that have body? e.g. not sure if much point emitting pull requests here
            summary = e.summary
            body = e.body
            if body is None:
                lines = summary.splitlines(keepends=True)
                if len(lines) > 1:
                    summary = lines[0].strip()
                body = ''.join(lines[1:]) # todo meh. hacky, better to extract bodies in the provider properly
            if body.strip() == '':
                body = None

            yield node(
                dt_heading(
                    e.dt,
                    link(url=e.link, title=summary) if e.link is not None else summary
                ),
                body=None if body is None else pandoc.to_org(body, from_='gfm'), # github flavored markdown
            )


if __name__ == '__main__':
    Github.main()
