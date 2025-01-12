"""Generate the code reference pages and navigation for documentation with MKDocs."""

import mkdocs_gen_files
from pathlib import Path

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
src = root / "snappylapy"

for path in sorted(src.rglob("*.py")):
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

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
