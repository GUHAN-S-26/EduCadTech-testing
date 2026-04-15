import os
from bs4 import BeautifulSoup

proj_dir = "d:/Freelancing/Project 2"
html_files = [f for f in os.listdir(proj_dir) if f.endswith('.html') and os.path.isfile(os.path.join(proj_dir, f))]

for file in html_files:
    path = os.path.join(proj_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    pagination_parts = soup.find_all("ul", class_="pagination-part")
    
    if pagination_parts:
        for p in pagination_parts:
            # remove the div containing it as well if it's just a wrapper
            parent_div = p.parent
            p.decompose()
            if parent_div and parent_div.name == "div" and "pagination-area" in parent_div.get("class", []):
                if not parent_div.get_text(strip=True):
                    parent_div.decompose()
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Removed pagination from {file}")

print("Done.")
