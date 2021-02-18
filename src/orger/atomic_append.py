from pathlib import Path
from os.path import lexists
import logging
from typing import Union

PathIsh = Union[str, Path]

def atomic_append_raw(
        path: PathIsh,
        data: str,
) -> None:
    path = Path(path)
    # https://stackoverflow.com/a/13232181
    enc = data.encode('utf8')
    # TODO handle windows properly? https://www.notthewizard.com/2014/06/17/are-files-appends-really-atomic/
    if len(enc) > 4096:
        logging.warning("writing out %s might be non-atomic (see https://stackoverflow.com/a/1154599/706389)", data)
    with path.open('ab') as fo:
        fo.write(enc)


# TODO might be useful in other projects?
def assert_not_edited(path: Path) -> None:
    vim = '.' + path.name + '.swp'
    emacs = '.#' + path.name
    for x in [vim, emacs]:
        lf = path.parent / x
        if lexists(lf): # lexist is necessary because emacs uses symlink for lock file
            raise RuntimeError('File is being edited: {}'.format(lf))


def atomic_append_check(
        path: PathIsh,
        data: str,
) -> None:
    """
    This is editor (emacs/vim)-aware and checks for existence of swap file first.
    Not fully atomic, but hopefully atomic enough for all practical purposes
    TODO make it configurabe if user has different swap file patterns for some reason?
    """
    # may be a bit too paranoid, but perhaps doesn't hurt.
    path = Path(path)
    assert_not_edited(path)
    atomic_append_raw(path, data)


def test_atomic_append_check(tmp_path: Path) -> None:
    of = tmp_path / 'test.org'
    of.touch()

    import pytest # type: ignore

    from subprocess import Popen, PIPE, check_call
    from time import sleep

    from contextlib import contextmanager
    @contextmanager
    def tmp_popen(*args, **kwargs):
        with Popen(*args, **kwargs) as p:
            try:
                yield p
            finally:
                p.terminate()

    atomic_append_check(of, 'data1')
    atomic_append_check(of, 'data2')
    assert of.read_text() == 'data1data2'

    with tmp_popen(['vi', '-c', 'startinsert', str(of)], stdin=PIPE, stdout=PIPE, stderr=PIPE) as p: # enter insert mode
        for attempt in range(10):
            # ugh, needs long pause for some reason
            sleep(1)
            swapfiles = list(tmp_path.glob('.*.swp'))
            if len(swapfiles) > 0:
                break
        else:
            raise AssertionError(f'Expected swapfiles in {tmp_path}')

        with pytest.raises(Exception):
            # Expected to raise due to being edited by vim
            atomic_append_check(of, 'test')
