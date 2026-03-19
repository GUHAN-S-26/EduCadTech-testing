import urllib.request
import os

print("Fetching correct templates...")

templates = {
    "template_index.html": "https://keenitsolutions.com/products/html/educavo/index.html",
    "template_about.html": "https://keenitsolutions.com/products/html/educavo/about2.html",
    "template_course.html": "https://keenitsolutions.com/products/html/educavo/course2.html",
    "template_contact.html": "https://keenitsolutions.com/products/html/educavo/contact2.html",
}

for filename, url in templates.items():
    print(f"Downloading {url} to {filename}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(filename, "wb") as f:
                f.write(response.read())
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

print("Templates downloaded successfully.")
