import bs4

files = ['index.html', 'about.html', 'courses.html', 'contact.html', 'verify.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Find footer-bottom
    footer_bottom = soup.find(class_='footer-bottom')
    if footer_bottom:
        row = footer_bottom.find(class_='row')
        if row:
            # Clear existing columns
            row.clear()
            
            # Create a single 12-column centered div
            new_col = soup.new_tag('div', attrs={'class': 'col-lg-12 text-center'})
            
            # Add the copyright div inside
            copyright_div = soup.new_tag('div', attrs={'class': 'copyright'})
            
            # Ensure the inner p isn't forcing inline alignment we don't want,
            # wait, text-center on col-lg-12 usually does the trick, but let's add p tag.
            p_tag = soup.new_tag('p')
            p_tag.string = '© 2026 EduCadTech. All Rights Reserved.'
            
            copyright_div.append(p_tag)
            new_col.append(copyright_div)
            row.append(new_col)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Copyright text centered in all files.")
