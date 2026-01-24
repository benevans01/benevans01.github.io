import re

input_file = "raw_lenses.txt"
output_file = "clean_lenses.js"

def sanitize():
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Split by commas to get individual items
        # We assume the list is comma-separated
        items = content.split(',')

        clean_items = []
        for item in items:
            # Clean up whitespace and quotes around the word
            clean_word = item.strip().strip('"').strip("'")
            
            # Skip empty items
            if not clean_word:
                continue
                
            # FIX 1: Replace Smart Quotes with straight quotes if any remain inside
            clean_word = clean_word.replace('“', "'").replace('”', "'")
            
            # FIX 2: Escape double quotes inside the word (e.g., "He said "Hello"")
            clean_word = clean_word.replace('"', '\\"')

            clean_items.append(clean_word)

        # Write to output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("const lenses = [\n")
            
            # Write 5 items per line
            chunk_size = 5
            for i in range(0, len(clean_items), chunk_size):
                chunk = clean_items[i:i + chunk_size]
                # Format as: "Item", "Item",
                line_str = ', '.join([f'"{x}"' for x in chunk])
                f.write(f"    {line_str},\n")
                
            f.write("];")

        print(f"Success! Processed {len(clean_items)} lenses.")
        print(f"Open '{output_file}' and copy the code.")

    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'.")

if __name__ == "__main__":
    sanitize()