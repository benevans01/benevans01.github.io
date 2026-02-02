from pathlib import Path
import re

INPUT_FILE = "lenses_cleaned.js"
OUTPUT_FILE = "lenses_flat.js"

src = Path(INPUT_FILE).read_text(encoding="utf-8")

def flatten_array_block(text: str) -> str:
    pattern = r"(const\s+lenses\s*=\s*\[)(.*?)(\]\s*;)"
    def repl(match):
        before, body, after = match.groups()
        # IMPORTANT: do not touch quotes at all, just whitespace
        body_flat = " ".join(body.split())
        # No comma normalization for now to avoid introducing new chars
        # body_flat = re.sub(r",\s*", ", ", body_flat)
        flat_line = before + body_flat + after
        print("Flat line length:", len(flat_line))
        print("First 200 chars:\n", flat_line[:200])
        print("Last 200 chars:\n", flat_line[-200:])
        return flat_line
    return re.sub(pattern, repl, text, flags=re.DOTALL)

flat = flatten_array_block(src)
Path(OUTPUT_FILE).write_text(flat, encoding="utf-8")

print(f"Written flattened file to {OUTPUT_FILE}")
