from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable

from atomicwrites import atomic_write  # type: ignore[import-untyped]

State = dict[str, Any]


# TODO hmm. state should be ordered ideally? so it's easy to add/remove items?
# would require storing as list of lists? or use that https://stackoverflow.com/a/6921760/706389
class JsonState:
    def __init__(
        self,
        path: Path | str,
        *,
        dry_run: bool = False,
        default: State | None = None,
        logger: logging.Logger = logging.getLogger('orger'),  # noqa: B008
    ) -> None:
        self.path = Path(path)
        self.dry_run = dry_run

        if default is None:
            default = {}
        self.default = default

        self.state: State | None = None
        self.logger = logger
        # TODO for simplicity, write empty if file doesn't exist??

    def __contains__(self, key: str) -> bool:
        return key in self.get()

    def __setitem__(self, key: str, value: Any) -> None:
        current = self.get()
        assert key not in current  # just in case
        current[key] = value

        if self.dry_run:
            self.logger.debug('dry run! ignoring %s: %s', key, value)
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with atomic_write(str(self.path), overwrite=True) as fo:
            json.dump(current, fo, indent=1, sort_keys=True)

    def get(self) -> State:
        if self.state is None:
            if not self.path.exists():
                self.state = self.default
            else:
                with self.path.open('r') as fo:
                    self.state = json.load(fo)
        return self.state

    def feed(self, key: str, value: Any, action: Callable[[], None]) -> None:
        # just to be safe so we don't dump int by accident
        assert isinstance(key, str), f"key/id has to be a str! key: {key!r}, value: {value!r}"

        if key in self:
            self.logger.debug('already handled: %s: %s', key, value)
            return
        self.logger.info('adding new item %s: %s', key, value)
        action()
        self[key] = repr(value)


def test_state(tmp_path: Path) -> None:
    import pytest

    path = tmp_path / 'state.json'
    state = JsonState(path)

    def mtime() -> float:
        return path.stat().st_mtime

    assert not path.exists()

    res = []

    def feed(k, v):
        def action() -> None:
            res.append(v)

        state.feed(k, v, action=action)

    feed('a', 123)
    assert res == [123]

    m1 = mtime()

    feed('a', 456)
    assert res == [123]

    assert mtime() == m1  # shouldn't touch file at all

    state = JsonState(path)

    assert mtime() == m1  # shouldn't touch either

    feed('b', 'abacaba')

    m2 = mtime()

    assert res == [123, 'abacaba']
    feed('a', None)
    assert res == [123, 'abacaba']

    assert mtime() == m2

    # shouldn't trigger because item is already present
    state.feed('a', 'err', lambda: None.whatever)  # type: ignore[attr-defined]

    with pytest.raises(AttributeError):
        state.feed('hiii', 'error 2 ', lambda: None.whatever)  # type: ignore[attr-defined]

    assert mtime() == m2  # shouldn't corrupt or modify the file

    state = JsonState(path, dry_run=True)
    feed('c', 'c')
    feed('x', 'y')
    feed('a', 'whatever')

    assert res == [123, 'abacaba', 'c', 'y']
    assert mtime() == m2  # should't modify state in dry run mode
