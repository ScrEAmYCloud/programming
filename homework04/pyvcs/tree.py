import pathlib
import stat
import time
import typing as tp
import os

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_inputs = []
    for entry in index:
        _, title = os.path.split(entry.name)
        if dirname:
            titles = dirname.split("/")
        else:
            titles = entry.name.split("/")
        if len(titles) != 1:
            prefix = titles[0]
            title = f"/".join(titles[1:])
            mode = "40000"
            tree_input = f"{mode} {prefix}\0".encode()
            tree_input += bytes.fromhex(write_tree(gitdir, index, title))
            tree_inputs.append(tree_input)
        else:
            if dirname and entry.name.find(dirname) == -1:
                continue
            with open(entry.name, "rb") as file:
                info = file.read()
            mode = str(oct(entry.mode))[2:]
            tree_input = f"{mode} {title}\0".encode()
            tree_input += bytes.fromhex(hash_object(info, "blob", write=True))
            tree_inputs.append(tree_input)

    tree_binary = b"".join(tree_inputs)
    return hash_object(tree_binary, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if author is None and "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ:
        author = (
            str(os.getenv("GIT_AUTHOR_NAME", None) + " " + f'<{os.getenv("GIT_AUTHOR_EMAIL", None)}>'))  # type:ignore
    now = int(time.mktime(time.localtime()))
    tz = time.timezone
    if tz > 0:
        tz_str = "-"
    else:
        tz_str = "+"
    tz_str += f"{abs(tz) // 60 // 60:02}{abs(tz) // 60 % 60:02}"
    cont = [f"tree {tree}"]
    if parent is not None:
        cont.append(f"parent {parent}")
    cont.append(f"author {author} {now} {tz_str}")
    cont.append(f"committer {author} {now} {tz_str}")
    cont.append(f"\n{message}\n")
    return hash_object("\n".join(cont).encode(), "commit", write=True)