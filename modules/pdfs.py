#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading, setup_logger

import logging
from datetime import datetime

import my.pdfs as pdfs


class PdfView(StaticView):
    def get_items(self):
        for pdf in sorted(
                pdfs.get_annotated_pdfs(),
                key=lambda p: datetime.min if p.date is None else p.date.replace(tzinfo=None),
        ):
            yield node(
                dt_heading(pdf.date, str(pdf.path)),
                children=[node(
                    dt_heading(a.date, f'page {a.page} {a.highlight or ""}'),
                    body=a.comment,
                ) for a in pdf.annotations]
            )


if __name__ == '__main__':
    setup_logger(pdfs.get_logger(), level=logging.DEBUG)
    PdfView.main()
