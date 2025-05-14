#!/usr/bin/env python3
from datetime import datetime

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import docview_link, literal, node


class PdfView(Mirror):
    def get_items(self) -> Mirror.Results:
        import my.pdfs as pdfs

        for pdf in sorted(
            pdfs.annotated_pdfs(),
            key=lambda p: datetime.min if isinstance(p, Exception) or p.created is None else p.created.replace(tzinfo=None),
        ):
            if isinstance(pdf, Exception):
                yield error(pdf)
                continue

            def chit(pdf: pdfs.Pdf):
                for a in pdf.annotations:
                    parts = []
                    # fmt: off
                    highlight = (a.highlight or '').strip()
                    author    = (a.author    or '').strip()
                    comment   = (a.comment   or '').strip()
                    # fmt: on
                    if highlight:
                        parts.append(literal(highlight))
                    if author:
                        parts.append(f'by {author}')
                    if comment:
                        parts.append(comment)
                    body = '\n'.join(parts)
                    page1 = a.page + 1
                    page_link = docview_link(path=pdf.path, title=f'page {page1}', page1=page1)
                    yield node(
                        dt_heading(a.created, page_link),
                        body=body,
                    )

            pdf_link = docview_link(path=pdf.path, title=str(pdf.path))  # todo would be nice to extract metadata for title
            yield node(dt_heading(pdf.created, pdf_link), children=list(chit(pdf)))


if __name__ == '__main__':
    # import logging
    # from orger.common import setup_logger
    # setup_logger(pdfs.logger, level=logging.DEBUG)
    PdfView.main()
