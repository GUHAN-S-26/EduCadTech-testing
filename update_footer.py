import bs4

footer_html = """
<div class="col-lg-3 col-md-12 col-sm-12 footer-widget md-mb-50">
    <div class="footer-logo mb-30">
        <a href="index.html"><img alt="EduCadTech Logo" src="images/logo.png" /></a>
    </div>
    <div class="textwidget pr-60 md-pr-15">
        <p class="white-color">We are EduCadTech, providing expert-led courses to help you advance your career. We empower learners with knowledge and practical skills.</p>
    </div>
</div>
<div class="col-lg-3 col-md-12 col-sm-12 footer-widget md-mb-50">
    <h3 class="widget-title">Quick Links</h3>
    <ul class="site-map">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="courses.html">Courses</a></li>
        <li><a href="verify.html">Verify Certificate</a></li>
        <li><a href="contact.html">Contact</a></li>
    </ul>
</div>
<div class="col-lg-3 col-md-12 col-sm-12 footer-widget md-mb-50">
    <h3 class="widget-title">Contact Info</h3>
    <ul class="address-widget">
        <li>
            <i class="flaticon-location"></i>
            <div class="desc">374 William S Canning Blvd, River MA 2721, USA</div>
        </li>
        <li>
            <i class="flaticon-call"></i>
            <div class="desc">
                <a href="tel:(+880)155-69569">(+880)155-69569</a>
            </div>
        </li>
        <li>
            <i class="flaticon-email"></i>
            <div class="desc">
                <a href="mailto:info@EduCadTech.com">info@EduCadTech.com</a>
            </div>
        </li>
    </ul>
</div>
<div class="col-lg-3 col-md-12 col-sm-12 footer-widget">
    <h3 class="widget-title">Social Media</h3>
    <ul class="footer_social">
        <li>
            <a href="#" target="_blank"><span><i class="fa fa-facebook"></i></span></a>
        </li>
        <li>
            <a href="# " target="_blank"><span><i class="fa fa-twitter"></i></span></a>
        </li>
        <li>
            <a href="# " target="_blank"><span><i class="fa fa-pinterest-p"></i></span></a>
        </li>
        <li>
            <a href="# " target="_blank"><span><i class="fa fa-google-plus-square"></i></span></a>
        </li>
        <li>
            <a href="# " target="_blank"><span><i class="fa fa-instagram"></i></span></a>
        </li>
    </ul>
</div>
"""

files = ['index.html', 'about.html', 'courses.html', 'contact.html', 'verify.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    footer = soup.find('footer', id='rs-footer')
    if footer:
        footer_top = footer.find('div', class_='footer-top')
        if footer_top:
            row = footer_top.find('div', class_='row')
            if row:
                row.clear()
                row.append(bs4.BeautifulSoup(footer_html, 'html.parser'))
                
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Footers updated in all files.")
