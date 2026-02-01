import requests
from bs4 import BeautifulSoup
import json

# URL of the Stanford Encyclopedia of Philosophy Table of Contents
URL = "https://plato.stanford.edu/contents.html"
BASE_URL = "https://plato.stanford.edu/"

print("Contacting the Stanford Encyclopedia...")
try:
    response = requests.get(URL)
    response.raise_for_status() # Check for errors
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main list of entries
    # The SEP contents page usually lists entries in a div with id 'content' or similar, 
    # but simply looking for all links containing "entries/" is the most robust method.
    entries = []
    
    # Get all links
    links = soup.find_all('a')
    
    for link in links:
        href = link.get('href')
        title = link.get_text()
        
        # Filter for actual entry links
        if href and "entries/" in href and title:
            # Clean up the title (remove newlines/extra spaces)
            clean_title = " ".join(title.split())
            
            # Construct full URL
            full_url = BASE_URL + href
            
            # Create the object
            entry_obj = {
                "title": clean_title,
                "link": full_url
            }
            
            entries.append(entry_obj)

    # Remove duplicates if any (based on link)
    seen = set()
    unique_entries = []
    for d in entries:
        if d['link'] not in seen:
            seen.add(d['link'])
            unique_entries.append(d)

    print(f"Successfully scraped {len(unique_entries)} articles.")

    # --- SAVE TO FILE ---
    # We write this directly as a JavaScript file so you can use it immediately.
    with open("sep_data.js", "w", encoding="utf-8") as f:
        f.write("// AUTO-GENERATED SEP DATABASE\n")
        f.write("const articles = ")
        # indent=4 makes it readable, verify the format fits JS syntax
        json_string = json.dumps(unique_entries, indent=4)
        f.write(json_string)
        f.write(";")

    print("Done! Open 'sep_data.js' and copy the content to your main data file.")

except Exception as e:
    print(f"Error occurred: {e}")