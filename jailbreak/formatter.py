# --- CONFIGURATION ---
input_file = "raw_list.txt"      # The name of your file with the list of nouns
output_file = "formatted_js.txt" # The file this script will create

def format_list():
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Read lines and strip whitespace/newlines
            lines = [line.strip() for line in f if line.strip()]

        # Open the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            # Loop through lines and format them
            # We add a newline every 5 items to keep your code readable
            for i, line in enumerate(lines):
                # The formatting magic: "Word", 
                f.write(f'"{line}", ')
                
                # Add a line break every 5 items so your JS doesn't scroll forever
                if (i + 1) % 5 == 0:
                    f.write('\n')
        
        print(f"Success! Processed {len(lines)} items.")
        print(f"Open '{output_file}' and copy the text.")

    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'. Make sure it's in the same folder.")

if __name__ == "__main__":
    format_list()