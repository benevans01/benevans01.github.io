from pathlib import Path

text = Path("input.txt").read_text(encoding="cp1252", errors="ignore")
one_line = " ".join(text.split())
print(one_line)

