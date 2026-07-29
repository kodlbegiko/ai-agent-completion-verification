from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path

PAGE_W, PAGE_H = 612, 792
LEFT, TOP = 48, 744
FONT_SIZE, LEADING = 9, 12
LINES_PER_PAGE = 56


def plain_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        line = re.sub(r"^#{1,6}\s*", "", line)
        line = line.replace("**", "").replace("`", "").replace("–", "-").replace("—", "-")
        if line.startswith("|---"):
            continue
        if line.startswith("|"):
            line = "  ".join(part.strip() for part in line.strip("|").split("|"))
        if not line:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(line, width=94, break_long_words=False, break_on_hyphens=False) or [""])
    return lines


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(lines: list[str]) -> bytes:
    pages = [lines[i:i + LINES_PER_PAGE] for i in range(0, len(lines), LINES_PER_PAGE)] or [[]]
    objects: list[bytes] = []
    # 1 catalog, 2 pages tree, 3 font, then pairs of page/content objects.
    kids = []
    for index in range(len(pages)):
        kids.append(f"{4 + index * 2} 0 R")
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for index, page_lines in enumerate(pages):
        page_obj = 4 + index * 2
        content_obj = page_obj + 1
        content_parts = [f"BT /F1 {FONT_SIZE} Tf {LEFT} {TOP} Td {LEADING} TL"]
        for line_no, line in enumerate(page_lines):
            if line_no:
                content_parts.append("T*")
            content_parts.append(f"({esc(line)}) Tj")
        content_parts.append("ET")
        stream = "\n".join(content_parts).encode("latin-1", errors="replace")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_obj} 0 R >>".encode())
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode())
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects)+1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    source = Path(args.input)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(build_pdf(plain_lines(source.read_text(encoding="utf-8"))))
    print(target)


if __name__ == "__main__":
    main()
