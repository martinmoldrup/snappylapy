"""Read the markdown file and extract all the code blocks and put them into tests."""
import pathlib
import re

codeblock_opening = r'^```python'
codeblock_closing = r'^```'

PATH = pathlib.Path(__file__).parent.parent / "README.md"
PATH_SAVE_DIR = pathlib.Path(__file__).parent.parent / "readme-examples"

def extract_codeblocks(filepath: pathlib.Path) -> list[str]:
    """Extract code blocks from a markdown file."""
    code_blocks: list[str] = []
    in_code_block = False
    current_block: str = ""

    with filepath.open("r", encoding="utf-8") as file:
        for line in file:
            if re.match(codeblock_opening, line):
                in_code_block = True
                current_block = ""
            elif re.match(codeblock_closing, line) and in_code_block:
                in_code_block = False
                code_blocks.append(current_block.strip())
            elif in_code_block:
                current_block += line

    return code_blocks


def save_codeblocks(code_blocks: list[str], save_dir: pathlib.Path) -> None:
    """Save code blocks to files."""
    save_dir.mkdir(exist_ok=True)
    for i, block in enumerate(code_blocks):
        with (save_dir / f"example_{i}.py").open("w", encoding="utf-8") as file:
            file.write(block)

code_blocks = extract_codeblocks(PATH)
save_codeblocks(code_blocks, PATH_SAVE_DIR)
