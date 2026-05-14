import subprocess
import json
import os

_viewer_proc = None
_viewer_paths = [
    os.path.join(os.path.dirname(__file__), "vector_shower"),
    "/home/quazyrog/Desktop/MdCS2026/repo_/vector_shower/cmake-build-debug-system/vector_shower",
]
_debug = False


def _put_command(cmd, **kwargs):
    kwargs["__cmd__"] = cmd
    cmd = json.dumps(kwargs)
    if _debug:
        print(f"Sending command: {cmd!r}")
    global _viewer_proc
    if _viewer_proc is None or _viewer_proc.poll() is not None:
        _viewer_proc = _require_one(
            RuntimeError(
                f"Cannot start vector_shower from any of paths: {_viewer_paths}"
            ),
            (
                (
                    lambda: subprocess.Popen(
                        p,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.DEVNULL if not _debug else None,
                        stderr=subprocess.STDOUT,
                    )
                )
                for p in _viewer_paths
            ),
        )
    _viewer_proc.stdin.write(cmd.encode("utf-8") + b"\n")
    _viewer_proc.stdin.flush()


def _require_one(err, fns):
    for fn in fns:
        try:
            return fn()
        except:
            pass
    raise err


def _xy(veclike):
    x = _require_one(
        ValueError(f"Nie mogę odczytać współrzędnej x z {veclike}"),
        [
            lambda: veclike.x,
            lambda: veclike[0],
            lambda: veclike[0, 0],
            lambda: veclike.get(0, 0),
        ],
    )
    y = _require_one(
        ValueError(f"Nie mogę odczytać współrzędnej y z {veclike}"),
        [
            lambda: veclike.x,
            lambda: veclike[1],
            lambda: veclike[1, 0],
            lambda: veclike.get(1, 0),
        ],
    )
    return x, y


def _test():
    vs = []
    for i in range(1000):
        vs.append((i / 100, i / 100))
    show_vector((0, 0))
    show_vector_cloud(vs)
    show_vector((1, 1))
    vs = []
    for x in range(100):
        for y in range(100):
            vs.append((6 + x / 100, 1 + y / 100))
    show_vector_cloud(vs)
    vs = []
    for x in range(50):
        for y in range(50):
            vs.append((6.25 + x / 100, 1.25 + y / 100))
    show_vector_cloud(vs)


def show_vector(vec, color="#19814a"):
    x, y = _xy(vec)
    _put_command("add_vector", x=x, y=y, color=color)


def show_vector_cloud(vectors, color="#108bee"):
    xs = []
    ys = []
    for vec in vectors:
        x, y = _xy(vec)
        xs.append(x)
        ys.append(y)
    _put_command("add_vector_swarm", xs=xs, ys=ys, color=color)


if __name__ == "__main__":
    _test()
