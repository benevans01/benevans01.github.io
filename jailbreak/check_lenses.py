from pathlib import Path

INPUT_FILE = "lenses_raw.js"
OUTPUT_FILE = "lenses_cleaned.js"

text = Path(INPUT_FILE).read_text(encoding="utf-8", errors="ignore")

# 1. Normalize curly quotes to straight quotes
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

lines = text.splitlines()
problems = []

clean_lines = []

for i, line in enumerate(lines, start=1):
    # Count double and single quotes on this line
    double_quotes = line.count('"')
    single_quotes = line.count("'")

    # Very simple heuristic: in a JS array of strings, most item lines should
    # have 2 double-quotes (start + end of string).
    if "const lenses" in line or line.strip().startswith("//"):
        # skip header or comments
        pass
    else:
        if "[" in line or "]" in line:
            # the opening/closing bracket lines may not have quotes
            pass
        else:
            if double_quotes not in (0, 2):
                problems.append(
                    f"Line {i}: suspicious number of double quotes ({double_quotes}) -> {line!r}"
                )

    clean_lines.append(line)

clean_text = "\n".join(clean_lines)
Path(OUTPUT_FILE).write_text(clean_text, encoding="utf-8")

print(f"Cleaned file written to {OUTPUT_FILE}")
if problems:
    print("\nPotential quote problems found:")
    for p in problems[:50]:
        print(p)
    if len(problems) > 50:
        print(f"...and {len(problems) - 50} more")
else:
    print("No obvious per-line quote count issues detected.")
