#!/usr/bin/env python3
import logging

from my.instapaper import get_pages # type: ignore

from kython import group_by_key
from kython.klogging import setup_logzero
from kython.org_tools import as_org_entry as as_org

def get_logger():
    return logging.getLogger('instapaper-org-view')

def main():
    logger = get_logger()
    setup_logzero(logger, level=logging.DEBUG)

    for page in get_pages():
        bm = page.bookmark
        print(as_org(
            todo=False,
            level=1,
            created=bm.dt,
            inline_created=True,
            heading=f'{bm.title} {bm.url}',
            body=bm.instapaper_link,
            # TODO make sure as_org figures out the date
        ).strip())
        # TODO autostrip could be an option for formatter

        for hl in page.highlights:
            print(as_org(
                todo=False,
                level=2,
                created=hl.dt,
                inline_created=True,
                heading=hl.text, # TODO hmmm, what if it's multiple lines?
                body=hl.instapaper_link,
            ).strip())
        # TODO could put links in org mode links? so not as much stuff is displayed?
        # TODO reverse order? not sure...
        # TODO unique id meaning that instapaper manages the item?
    # for k, gr in groups.items():
    #     ss = sorted(gr, key=lambda h: h.dt)
    #     rep = ss[0] # TODO repr should be bookmark?
    #     import ipdb; ipdb.set_trace() 
    #     print(ss)
    #     # use ss.url and ss.title
    #     # use ss.dt for org timestamp
    #     # use text and note if it's not None
    #     # TODO as_org_entry is gonna be more tricky now...



    pass

if __name__ == '__main__':
    main()
