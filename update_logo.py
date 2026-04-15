import bs4

files = ['index.html', 'about.html', 'courses.html', 'contact.html', 'verify.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Update header logos
    logos = soup.find_all('img', alt='EduCadTech Logo')
    for logo in logos:
        classes = logo.get('class', [])
        if 'normal-logo' in classes:
            logo['src'] = 'images/lite-logo.png'
            logo['style'] = 'width: 181.61px; height: 30.31px; max-height: none;'
        elif 'sticky-logo' in classes:
            logo['src'] = 'images/dark-logo.png'
            logo['style'] = 'width: 181.61px; height: 30.31px; max-height: none;'
        elif logo.parent and 'footer-logo' in logo.parent.get('class', []):
            logo['src'] = 'images/lite-logo.png'
            
    # Also update preloader logo
    loader_icons = soup.select('.loader-icon img')
    for img in loader_icons:
        img['src'] = 'images/lite-logo.png'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Logos swapped to template originals in all files.")
