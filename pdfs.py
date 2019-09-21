#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from datetime import datetime
from kython.kerror import unwrap

from my.reading import pdfs

class PdfView(StaticView):
    def get_items(self):
        from pathlib import Path
        for pdf in sorted(
                pdfs.get_annotated_pdfs(),
                key=lambda p: datetime.min if p.date is None else p.date.replace(tzinfo=None),
        ):
            yield f'pdf_annotation_{pdf.path}', node(
                dt_heading(pdf.date, str(pdf.path)),
                children=[node(
                    dt_heading(a.date, f'page {a.page} {a.highlight or ""}'),
                    body=a.comment,
                ) for a in pdf.annotations]
            )


if __name__ == '__main__':
    PdfView.main()
