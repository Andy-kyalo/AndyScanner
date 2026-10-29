#!/usr/bin/env python3
"""Build a verified release ZIP from an exact committed Git revision."""
import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

EXCLUDED_PARTS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "node_modules", ".venv", "venv",
}
EXCLUDED_NAMES = {
    ".env", "id_rsa", "id_ed25519", "credentials",
    "credentials.json", "secrets", "secrets.json",
    "secrets.yaml", "secrets.yml", "token", "tokens",
}
EXCLUDED_SUFFIXES = (
    ".pyc", ".pyo", ".log", ".sqlite", ".sqlite3", ".db",
    ".bak", ".backup", ".pem", ".key", ".p12", ".pfx",
    ".jks", ".keystore", ".dump", ".sql", ".orig", ".old",
    ".swp", ".tmp", ".save", "~",
)
EXCLUDED_PREFIXES = (".env.",)
EXCLUDED_DIRS = {"logs", "cache", "caches"}
MANIFEST = "RELEASE-REVISION.txt"


def safe_member(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        return False
    if any(part.lower() in EXCLUDED_PARTS | EXCLUDED_DIRS for part in path.parts):
        return False
    base = path.name.lower()
    if base in EXCLUDED_NAMES or base.startswith(EXCLUDED_PREFIXES):
        return False
    return not base.endswith(EXCLUDED_SUFFIXES)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", default="dist/AndyScanner-release.zip")
    parser.add_argument("--revision", default="HEAD", help="committed Git revision (default: HEAD)")
    args = parser.parse_args()

    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
    status = git(root, "status", "--porcelain").decode()
    if status.strip():
        print("ERROR: working tree is not clean; commit or otherwise resolve changes before building.", file=sys.stderr)
        return 2

    try:
        revision = git(root, "rev-parse", "--verify", args.revision + "^{commit}").decode().strip()
    except subprocess.CalledProcessError:
        print("ERROR: revision is not a valid commit.", file=sys.stderr)
        return 2
    output = (root / args.output).resolve()
    if output == root or root not in output.parents:
        print("ERROR: output path must be inside the repository.", file=sys.stderr)
        return 2
    if output.exists():
        print("ERROR: output file already exists; refusing to overwrite it.", file=sys.stderr)
        return 2
    tree_paths = git(root, "ls-tree", "-r", "--name-only", "-z", revision).decode("utf-8", "surrogateescape").split(chr(0))
    if output.relative_to(root).as_posix() in tree_paths:
        print("ERROR: output path would overwrite a tracked file.", file=sys.stderr)
        return 2
    if output.relative_to(root).as_posix() == MANIFEST:
        print("ERROR: output path conflicts with the revision manifest.", file=sys.stderr)
        return 2

    raw_tree = git(root, "ls-tree", "-rz", "-r", "--full-tree", revision)
    entries = []
    for record in raw_tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_name = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        name = raw_name.decode("utf-8", "surrogateescape")
        if kind != "blob" or mode not in {"100644", "100755"}:
            continue
        if not safe_member(name) or name == MANIFEST:
            continue
        entries.append((name, oid, mode))

    if not entries:
        print("ERROR: no eligible committed files found.", file=sys.stderr)
        return 2

    manifest = (
        "AndyScanner release archive\n"
        f"Git revision: {revision}\n"
        f"Included files: {len(entries)}\n"
    ).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        prefix=f".{output.name}.",
        suffix=".tmp",
        dir=output.parent,
        delete=False,
    )
    temp_path = Path(handle.name)
    handle.close()

    try:
        with zipfile.ZipFile(temp_path, "w") as archive:
            for name, oid, mode in sorted(entries):
                data = git(root, "cat-file", "blob", oid)
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (int(mode, 8) & 0xFFFF) << 16
                archive.writestr(info, data)
            info = zipfile.ZipInfo(MANIFEST, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, manifest)

        with zipfile.ZipFile(temp_path) as archive:
            names = archive.namelist()
            bad = archive.testzip()
            unsafe = [name for name in names if name != MANIFEST and not safe_member(name)]
            if bad or unsafe or len(names) != len(set(names)):
                print(
                    f"ERROR: archive verification failed; bad_member={bad!r}; "
                    f"unsafe_count={len(unsafe)}",
                    file=sys.stderr,
                )
                return 2
            if archive.read(MANIFEST) != manifest:
                print("ERROR: revision manifest verification failed.", file=sys.stderr)
                return 2

        if output.exists():
            print("ERROR: output file appeared during build; refusing to overwrite it.", file=sys.stderr)
            return 2
        temp_path.replace(output)
    finally:
        temp_path.unlink(missing_ok=True)

    print(f"Release archive verified: {output}")
    print(f"Git revision: {revision}")
    print(f"Included files: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
