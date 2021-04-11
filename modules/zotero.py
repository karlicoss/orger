#!/usr/bin/env python3

from orger import Mirror
from orger.inorganic import node, link, docview_link, literal
from orger.common import dt_heading, error

from typing import Optional
from textwrap import indent, wrap

from more_itertools import bucket


class config:
    MAX_LINE_WIDTH: int = 120


colors_doc = """
To highlight tags based on color, add this to your Emacs config:
  (with-eval-after-load 'org
    (dolist (color '("yellow" "red" "purple" "blue" "green"))
        (add-to-list 'org-tag-faces
                     `(,color . (:background ,color)))))

NOTE: you'll need to restart emacs for this to take effect.
If some colors look too bright for you, you can just manually map them instead, e.g.:
  (with-eval-after-load 'org
    (add-to-list 'org-tag-faces '("red"   . (:foreground "#cc0000")))
    (add-to-list 'org-tag-faces '("green" . (:foreground "#00aa00"))))
"""


class Zotero(Mirror):
    DEFAULT_HEADER = Mirror.DEFAULT_HEADER + indent(colors_doc, '# ', lambda line: True)

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
                        # todo not sure about it here... maybe should rely on softwrap in emacs instead?
                        text = '\n'.join(wrap(text, width=config.MAX_LINE_WIDTH))
                        text = literal(text)
                        parts.append(text)
                    comment = a.comment
                    if comment is not None:
                        parts.append(comment)
                    page1 = a.page + 1  # NOTE: zotero using 0-indexing, pdfview using 1-indexing
                    body = '\n'.join(parts)

                    color = a.color_human
                    tags = list(a.tags)
                    # todo not sure which is best?
                    tags.append(color)
                    properties = {
                        'ZOTERO_COLOR': color,
                    }
                    if len(a.tags) > 0:
                        # zotero tags cal be multi-word? guess worth adding just in case
                        properties['ZOTERO_TAGS'] = ', '.join(a.tags)  # not sure what's the best separator...

                    # todo not sure about it...
                    mtodo: Optional[str] = None
                    if 'todo' in {t.lower() for t in tags}:
                        mtodo = 'TODO'

                    heading = docview_link(path=item.file, title=f'page {page1}', page1=page1)
                    if comment is not None:
                        # try to display first few words?
                        cline = wrap(comment, width=config.MAX_LINE_WIDTH)[0]
                        heading = heading + ' ' + cline
                    # todo would be nice to align tags, maybe...
                    yield node(
                        todo=mtodo,
                        heading=dt_heading(
                            a.added,
                            heading,
                        ),
                        tags=tags,
                        properties=properties,
                        body=body,
                    )
            body = ''
            if url := item.url:
                body = url
            yield node(
                heading=docview_link(path=item.file, title=item.title),
                tags=item.tags,
                body=body,
                children=list(chit())
            )

if __name__ == '__main__':
    Zotero.main()


# TODO maybe handle
# (see zotero-protocol-handler.js)
# zotero://pdf.js/viewer.html
# zotero://pdf.js/pdf/1/ABCD5678
