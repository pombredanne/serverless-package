import argparse
import fnmatch
import os
from pathlib import Path
import re
import zipfile

EXCLUDES = []


def add_arguments(parser):
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Specifies file to which the output is written.",
    )


def main():
    """
    Main entry point of the Comand
    """
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    # Find filepaths that should be added to the package
    excludes = find_excludes()
    paths = find_paths(excludes=excludes)
    if args.output:
        zip_package(paths=paths, fp=args.output)
    else:
        tree(paths)


def find_excludes():
    excludes = [
        ".*",  # Hidden files
    ]
    # Read .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with gitignore.open() as f:
            excludes += f.read().split("\n")
    else:
        raise ValueError("No .gitignore found")
    return excludes


def find_paths(excludes):
    """
    Finds the list of files that should be included in the archive‚
    """
    # Compile regex from list of glob exclusions
    exclusion_regex = re.compile(
        "|".join(fnmatch.translate(g.rstrip("/")) for g in excludes)
    )
    # Parse files and folders
    includes = []
    for root, dirs, files in os.walk(top=".", topdown=True):
        # Filter files that should be included
        for f in files:
            if not exclusion_regex.match(f):
                includes.append(Path(root, f))
        # Prune directories that match the exclude pattern
        dirs[:] = [Path(root, d) for d in dirs if not exclusion_regex.match(d)]
    return includes


def zip_package(paths, fp, compression=zipfile.ZIP_DEFLATED):
    """
    Takes a list of filepaths and compressed those files into a zip archive
    """
    with zipfile.ZipFile(
        file=fp, mode="w", compression=compression, compresslevel=9
    ) as z:
        for p in paths:
            z.write(p)


def tree(paths):
    """
    Displays a tree of the files about to be zipped
    """
    print("List of the files that would be included in the package:\n")
    for p in paths:
        depth = len(p.parts)
        spacer = "    " * (depth - 1)
        print(f"{spacer} {p.name}")
    print("\n", "To create the actual zip, you need to specify the --output parameter")


if __name__ == "__main__":
    main()
