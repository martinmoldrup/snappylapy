"""Read the markdown file and extract all the code blocks and put them into tests."""
from dataclasses import dataclass
import re
import pathlib
from toolit import tool

codeblock_opening = r'^\s*```python'
codeblock_closing = r'^\s*```'

PATH = pathlib.Path("snappylapy")
ADDITIONAL_PATHS = [
    pathlib.Path(__file__).parent.parent / "README.md",
]
PATH_SAVE_DIR = pathlib.Path(__file__).parent.parent / "tests" / "doc_examples"

@dataclass
class CodeBlock:
    text: str
    filename: str

class CodeBlockBuilder:
    """Build a single code block."""

    def __init__(self, opening_line: str, name: str) -> None:
        self.lines: list[str] = []
        self.indent_chars: str = self._extract_indent(opening_line)
        self.name = name

    def add_line(self, line_cleaned: str) -> None:
        line_cleaned = line_cleaned[len(self.indent_chars):]
        self.lines.append(line_cleaned)

    def _extract_indent(self, line: str) -> str:
        match = re.match(r'^\s*', line)
        return match.group(0) if match else ""

    def build(self) -> CodeBlock:
        return CodeBlock(text="\n".join(self.lines), filename=self.name)



def extract_codeblocks(filepath: pathlib.Path) -> list[CodeBlock]:
    """Extract code blocks from a markdown file."""
    code_blocks: list[CodeBlock] = []
    in_code_block = False

    with filepath.open("r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if re.match(codeblock_opening, line):
                in_code_block = True
                previous_line = lines[i - 1] if i > 0 else ""
                # Get text in between two ` chars from previous_line
                matches = re.findall(r'`([^`]*)`', previous_line)
                name = matches[0] if matches else f"test_example_{len(code_blocks)}"
                code_block_builder = CodeBlockBuilder(line, name)
            elif re.match(codeblock_closing, line) and in_code_block:
                in_code_block = False
                code_blocks.append(code_block_builder.build())
            elif in_code_block:
                code_block_builder.add_line(line)

    return code_blocks

def save_codeblocks(code_blocks: list[CodeBlock], save_dir: pathlib.Path) -> None:
    """Save code blocks to files."""
    if not code_blocks:
        return
    save_dir.mkdir(exist_ok=True, parents=True)
    for block in code_blocks:
        save_dir_file = save_dir / block.filename
        print(f"Saving code block to {save_dir_file}")
        with save_dir_file.open("w", encoding="utf-8") as file:
            file.write(block.text)

@tool
def extract_examples() -> None:
    """Extract examples from markdown and docstrings."""
    # Delete everything in the save directory
    # if PATH_SAVE_DIR.exists():
    #     for file in PATH_SAVE_DIR.iterdir():
    #         file.unlink()

    for path in PATH.rglob("*.py"):
        extract_and_save_codeblocks(path)

    for path in ADDITIONAL_PATHS:
        extract_and_save_codeblocks(path)

def extract_and_save_codeblocks(path: pathlib.Path) -> None:
    code_blocks = extract_codeblocks(path)
    savedir = PATH_SAVE_DIR / path.with_suffix("")
    save_codeblocks(code_blocks, savedir)


if __name__ == "__main__":
    extract_examples()
