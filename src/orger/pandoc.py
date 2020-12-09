"""
Helper for converting stuff to pandoc
"""
from functools import lru_cache
import logging
import shutil
from subprocess import run, PIPE
from typing import Optional


from .common import settings

@lru_cache(1)
def should_use_pandoc() -> bool:
    if not settings.USE_PANDOC:
        return False

    has_pandoc = shutil.which('pandoc') is not None
    if has_pandoc:
        return True

    import warnings
    warnings.warn("Install 'pandoc' to convert HTML to org-mode. See https://pandoc.org/installing.html")
    return False


def to_org(data: str, *, from_: str, logger=logging) -> str:
    if not should_use_pandoc():
        return data
    # TODO batch??

    # meh. for some reason they are converted to \\ otherwise
    if from_ == 'html':
        data = data.replace('<br>', '')
   
    try:
        r = run(
            ['pandoc', '-f', from_, '-t', 'org', '--wrap=none'],
            check=True,
            input=data.encode('utf8'),
            stdout=PIPE,
        )
    except Exception as e:
        logger.exception(e)
        return data # fallback
    res = r.stdout.decode('utf8')
    return res


def test():
    # html = "<p>and a <i>comment</i> too&nbsp;</p><p><br></p><p><b>multiline</b>!</p>"
    # TODO ok, it's annoying... not sure what to do with nonpritable crap
    html = "<p>and a <i>comment</i> too</p><p><br></p><p><b>multiline</b>!</p>"
    assert to_org(data=html, from_='html') == r'''
and a /comment/ too

*multiline*!
'''.lstrip()
