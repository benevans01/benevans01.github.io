import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://plato.stanford.edu/contents.html"
BASE_URL = "https://plato.stanford.edu/"

print("Contacting the Stanford Encyclopedia...")
try:
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    entries = []
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if href and "entries/" in href:
            full_url = BASE_URL + href.lstrip('/')
            entries.append(full_url)

    # dedupe
    entries = sorted(set(entries))

    def get_entry_title(entry_url):
        try:
            r = requests.get(entry_url)
            r.raise_for_status()
            s = BeautifulSoup(r.content, 'html.parser')

            # try main H1 first
            h1 = s.find('h1')
            if h1 and h1.get_text(strip=True):
                return h1.get_text(strip=True)

            # fallback: <title> tag, strip the trailing " - Stanford Encyclopedia of Philosophy"
            if s.title and s.title.string:
                title_text = s.title.string.strip()
                suffix = " - Stanford Encyclopedia of Philosophy"
                if title_text.endswith(suffix):
                    title_text = title_text[:-len(suffix)]
                return title_text

            return None
        except Exception as e:
            print(f"Error getting title for {entry_url}: {e}")
            return None

    output = []
    for i, url in enumerate(entries, start=1):
        print(f"[{i}/{len(entries)}] Fetching title for {url}")
        title = get_entry_title(url)
        if title:
            output.append({"title": title, "link": url})
        else:
            # fall back to last path component if all else fails
            slug = url.rstrip('/').split('/')[-1].replace('-', ' ')
            output.append({"title": slug, "link": url})
        time.sleep(0.5)  # be polite

    print(f"Successfully scraped {len(output)} articles.")

    with open("sep_data.js", "w", encoding="utf-8") as f:
        f.write("// AUTO-GENERATED SEP DATABASE\n")
        f.write("const articles = ")
        json_string = json.dumps(output, indent=4, ensure_ascii=False)
        f.write(json_string)
        f.write(";")

    print("Done! Open 'sep_data.js' and copy the content to your main data file.")

except Exception as e:
    print(f"Error occurred: {e}")
