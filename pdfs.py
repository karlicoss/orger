#!/usr/bin/env python3
from datetime import datetime
from kython.kerror import unwrap

from orger.org_view import OrgViewOverwrite, OrgWithKey
from orger.org_utils import OrgTree, as_org

from my.reading import pdfs

class PdfView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'pdf-view'

    def get_items(self):

        for pdf in sorted(pdfs.get_annotated_pdfs(), key=lambda p: datetime.min if p.date is None else p.date.replace(tzinfo=None)):
            yield f'pdf_annotation_{pdf.path}', OrgTree(
                as_org(
                    created=pdf.date,
                    heading=str(pdf.path),
                ),
                [
                    OrgTree(as_org(
                        created=a.date,
                        heading=f'page {a.page} {a.highlight or ""}',
                        body=a.comment,
                    )) for a in pdf.annotations
                ]
            )


def main():
    PdfView.main(default_to='pdfs.org')


if __name__ == '__main__':
    main()
