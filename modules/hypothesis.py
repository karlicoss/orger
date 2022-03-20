#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading, error

import my.hypothesis as hypothesis
import uuid
from typing import Optional, Mapping


class HypView(Mirror):
    def get_items(self) -> Mirror.Results:
        for page in hypothesis.pages():
            # TODO would be nice to signal error upwards? Maybe just yield Exception, rener it in Orger and allow setting error status?
            if isinstance(page, Exception):
                yield error(page)
                continue
            yield node(
                heading=dt_heading(page.created, link(title=page.title, url=page.url)),
                properties=self.get_page_properties(page),
                children=[
                    node(
                        heading=dt_heading(
                            hl.created, link(title="context", url=hl.hyp_link)
                        ),
                        properties=self.get_annotation_properties(hl),
                        tags=hl.tags,
                        body=hl.highlight,
                        children=[]
                        if hl.annotation is None
                        else [
                            node(
                                heading=self.get_annotation(hl.annotation).split("\n")[
                                    0
                                ],
                                body=self.get_annotation(hl.annotation),
                            )
                        ],
                    )
                    for hl in page.highlights
                ],
            )

    def get_annotation(self, annotation: Optional[str]) -> Optional[str]:
        assert self.cmdline_args is not None
        if not self.cmdline_args.markdown:
            return annotation

        from orger import pandoc

        org = pandoc.to_org(str(annotation), from_="markdown")
        return org

    def get_annotation_properties(
        self, highlight: hypothesis.Highlight
    ) -> Optional[Mapping[str, str]]:
        assert self.cmdline_args is not None
        if not self.cmdline_args.id_per_annotation:
            return None

        return {"ID": str(uuid.uuid3(uuid.NAMESPACE_URL, highlight.hyp_link))}

    def get_page_properties(self, page: hypothesis.Page) -> Optional[Mapping[str, str]]:
        assert self.cmdline_args is not None
        if not self.cmdline_args.id_per_page:
            return None

        return {"ID": str(uuid.uuid3(uuid.NAMESPACE_URL, page.url))}


# TODO tests for determinism
# TODO they could also be extracted to common routine and used in each provider
# TODO need to group by source??


def setup_parser(p) -> None:
    p.add_argument(
        "--markdown",
        action="store_true",
        help="Convert hypothesis markdown to org text",
    )
    p.add_argument(
        "--id-per-annotation", action="store_true", help="Add ID per annotation",
    )
    p.add_argument(
        "--id-per-page", action="store_true", help="Add ID per page",
    )


if __name__ == "__main__":
    HypView.main(setup_parser=setup_parser)
