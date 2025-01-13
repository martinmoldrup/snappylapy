"""Generate the code reference pages and navigation for documentation with MKDocs."""

import mkdocs_gen_files
from pathlib import Path
import subprocess


def generate_cli_docs():
    """Generate the CLI documentation."""
    type_gen_file_command = 'typer snappylapy/_cli.py utils docs --name snappylapy --title "Command Line Interface (CLI) for Snappylapy"'
    # Run the command and the stdout to the output file
    with mkdocs_gen_files.open("cli.md", "w") as output_file:
        result = subprocess.run(
            type_gen_file_command,
            shell=True,
            stdout=output_file,
        )
        if result.returncode != 0:
            raise ValueError(
                f"Command failed with return code {result.returncode}")


def generate_documentation_for_py_files(nav: mkdocs_gen_files.Nav) -> None:
    root = Path(__file__).parent.parent
    src = root / "snappylapy"

    python_files = src.rglob("*.py")

    # Sort the files to the top
    def sort_files(file: Path) -> int:
        """Sort to top and bottom."""
        sort_to_top = ["fixtures"]
        sort_to_bottom = ["constants"]
        if file.stem in sort_to_top:
            return 0
        if file.stem in sort_to_bottom:
            return 2
        return 1

    python_files = sorted(
        python_files,
        key=sort_files,
    )

    for path in python_files:
        doc_path = path.relative_to(src.parent).with_suffix(".md")
        full_doc_path = Path("reference", doc_path)
        parts = list(path.relative_to(src.parent).with_suffix("").parts)
        if path.stem == "__init__":
            # doc_path = doc_path.with_name("index.md")
            # full_doc_path = full_doc_path.with_name("index.md")
            # # delete the "__init__" element
            # parts.remove("__init__")
            continue
        if path.stem.startswith("_"):
            continue

        nav[parts] = doc_path.as_posix()

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            fd.write(f"::: {ident}")

        mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))


def generate_summary(nav: mkdocs_gen_files.Nav) -> None:
    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


if __name__ == "__main__":
    generate_cli_docs()
    nav = mkdocs_gen_files.Nav()
    generate_documentation_for_py_files(nav)
    generate_summary(nav)
