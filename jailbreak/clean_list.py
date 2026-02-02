from pathlib import Path
import re

# Change this to your filename
INPUT_FILE = "lenses.js"
OUTPUT_FILE = "lenses.cleaned.js"

# 1. Read file with forgiving encoding
text = Path(INPUT_FILE).read_text(encoding="utf-8", errors="ignore")

# 2. Normalize quotes (curly -> straight)
replacements = {
    "“": '"',
    "”": '"',
    "„": '"',
    "‟": '"',
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
}
for bad, good in replacements.items():
    text = text.replace(bad, good)

# 3. Optionally, ensure we use double quotes for this file
# (uncomment if you want to force everything to use ")
# text = text.replace("'", '"')

# 4. Collapse newlines and extra spaces inside the array declaration
#    This assumes the file is basically: const lenses = [ ... ];
#    and you want the ... part flattened.
def flatten_array_block(src: str) -> str:
    pattern = r"(const\s+lenses\s*=\s*\[)(.*?)(\]\s*;)"
    def repl(match):
        before, body, after = match.groups()
        # Collapse whitespace
        body_flat = " ".join(body.split())
        # Ensure comma+space formatting
        body_flat = re.sub(r",\s*", ', ', body_flat)
        return before + body_flat + after
    return re.sub(pattern, repl, src, flags=re.DOTALL)

cleaned = flatten_array_block(text)

# 5. Write cleaned output
Path(OUTPUT_FILE).write_text(cleaned, encoding="utf-8")

print(f"Written cleaned file to {OUTPUT_FILE}")
