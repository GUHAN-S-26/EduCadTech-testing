import bs4

files = ['index.html', 'about.html', 'courses.html', 'contact.html', 'verify.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Update all EduCadTech logos to 'images/logo.png'
    logos = soup.find_all('img', alt='EduCadTech Logo')
    for logo in logos:
        logo['src'] = 'images/logo.png'
        # Remove the style attr so we don't squash the new logo
        if 'style' in logo.attrs:
            del logo['style']
            
    # Also update preloader and loader icons if needed
    loader_icons = soup.select('.loader-icon img')
    for img in loader_icons:
        img['src'] = 'images/logo.png'
        if 'style' in img.attrs:
            del img['style']

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("All files updated to point to images/logo.png without inline style bounds.")
