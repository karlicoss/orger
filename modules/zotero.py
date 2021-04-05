#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, docview_link, literal
from orger.common import dt_heading, error

from typing import Optional
from textwrap import indent, wrap

from more_itertools import bucket


class Zotero(Mirror):
    def get_items(self) -> Mirror.Results:
        from my import zotero

        errors = []
        good = []
        for a in zotero.annotations():
            if isinstance(a, Exception):
                errors.append(a)
            else:
                good.append(a)

        for e in errors:
            yield error(e)


        groups = bucket(good, key=lambda a: a.item)
        for item in groups:
            file_annotations = groups[item]
            def chit():
                for a in file_annotations:
                    parts = []
                    text = a.text
                    if text is not None:
                        text = '\n'.join(wrap(text, width=150))  # todo make configurable?
                        text = literal(text)
                        parts.append(text)
                    comment = a.comment
                    if comment is not None:
                        parts.append(comment)
                    page1 = a.page + 1  # NOTE: zotero using 0-indexing, pdfview using 1-indexing
                    body = '\n'.join(parts)

                    # todo not sure about it...
                    mtodo: Optional[str] = None
                    if 'todo' in {t.lower() for t in a.tags}:
                        mtodo = 'TODO'

                    yield node(
                        heading=dt_heading(
                            a.added,
                            docview_link(path=item.file, title=f'on page {page1}', page1=page1)
                        ),
                        todo=mtodo,
                        body=body,
                        tags=a.tags,
                    )
            body = ''
            if url := item.url:
                body = url
            yield node(
                heading=docview_link(path=item.file, title=item.title),
                body=body,
                children=list(chit())
            )

if __name__ == '__main__':
    Zotero.main()


# TODO maybe handle
# (see zotero-protocol-handler.js)
# zotero://pdf.js/viewer.html
# zotero://pdf.js/pdf/1/ABCD5678
