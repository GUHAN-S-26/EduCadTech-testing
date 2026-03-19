import os
import re
import urllib.request
from bs4 import BeautifulSoup
import bs4
import cssutils
import logging

# Set up logging for cssutils to suppress warnings
cssutils.log.setLevel(logging.CRITICAL)

BASE_URL = "https://keenitsolutions.com/products/html/educavo/"

# Create directories
os.makedirs("css", exist_ok=True)
os.makedirs("js", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("assets/images", exist_ok=True)

html_files = {
    "index.html": "template_index.html",
    "about.html": "template_about.html",
    "courses.html": "template_course.html",
    "contact.html": "template_contact.html",
    "verify.html": "template_contact.html" 
}

css_registry = []
js_registry = []

def download_file(url, local_path):
    if not os.path.exists(local_path):
        try:
            print(f"Downloading {url} to {local_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
                dirname = os.path.dirname(local_path)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(content)
                return content
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return b""
    with open(local_path, "rb") as f:
        return f.read()

def process_css_content(content, base_url, css_path):
    # css_path is like 'assets/css/bootstrap.min.css' or 'style.css'
    # we are combining into 'css/style.css'
    
    # decode to string
    try:
        content_str = content.decode('utf-8', errors='ignore')
    except:
        return ""

    def replace_url(match):
        url = match.group(1).strip("'\"")
        if url.startswith("data:") or url.startswith("http"):
            return match.group(0)
        
        # calculate absolute url
        # absolute css url
        abs_css_dir = os.path.dirname(urllib.parse.urljoin(BASE_URL, css_path))
        abs_asset_url = urllib.parse.urljoin(abs_css_dir + "/", url)
        
        # calculate local path: typically we want it to map to our local structure
        # let's just put all assets referenced by CSS into our local relative to root
        # since our css is in css/, relative to css/ is '../'
        parsed_url = urllib.parse.urlparse(abs_asset_url)
        path = parsed_url.path
        # path is something like /products/html/educavo/assets/fonts/flaticon.woff
        # we want to save it as assets/fonts/flaticon.woff
        prefix = "/products/html/educavo/"
        if path.startswith(prefix):
            local_asset_path = path[len(prefix):] # e.g. assets/fonts/flaticon.woff
        else:
            local_asset_path = "assets/" + os.path.basename(path)
            
        # Download the asset
        download_file(abs_asset_url, local_asset_path)
        
        # Rewrite url for css/style.css to point to ../local_asset_path
        return f"url('../{local_asset_path}')"

    # Replace url(...)
    content_str = re.sub(r'url\((.*?)\)', replace_url, content_str)
    
    # Remove @import that are local and download them
    def replace_import(match):
        url = match.group(1).strip("'\"")
        if url.startswith("http"):
            return match.group(0)
        abs_css_dir = os.path.dirname(urllib.parse.urljoin(BASE_URL, css_path))
        abs_asset_url = urllib.parse.urljoin(abs_css_dir + "/", url)
        prefix = "/products/html/educavo/"
        parsed_url = urllib.parse.urlparse(abs_asset_url)
        path = parsed_url.path
        if path.startswith(prefix):
            local_asset_path = path[len(prefix):]
        else:
            local_asset_path = "assets/" + os.path.basename(path)
        
        imported_content = download_file(abs_asset_url, local_asset_path)
        return process_css_content(imported_content, BASE_URL, local_asset_path)

    content_str = re.sub(r'@import\s+(?:url\()?([\'"].*?[\'"])(?:\))?\s*;', replace_import, content_str)
    
    return content_str

all_css_content = ""
all_js_content = ""

# Process each template
import urllib.parse

for output_name, template_name in html_files.items():
    print(f"Processing {template_name} -> {output_name}")
    with open(template_name, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. Process CSS links
    css_links = soup.find_all("link", rel="stylesheet")
    for link in css_links:
        href = link.get("href")
        if href and not href.startswith("http"):
            if href not in css_registry:
                css_registry.append(href)
                abs_url = urllib.parse.urljoin(BASE_URL, href)
                content = download_file(abs_url, href)
                all_css_content += f"/* {href} */\n"
                all_css_content += process_css_content(content, BASE_URL, href) + "\n"
        link.decompose() # remove original link

    # Add the single CSS file
    new_css = soup.new_tag("link", rel="stylesheet", href="css/style.css")
    if soup.head:
        soup.head.append(new_css)

    # 2. Process JS scripts
    js_scripts = soup.find_all("script", src=True)
    for script in js_scripts:
        src = script.get("src")
        # Ignore external scripts like html5shiv
        if src and not src.startswith("http"):
            if src not in js_registry:
                js_registry.append(src)
                abs_url = urllib.parse.urljoin(BASE_URL, src)
                content = download_file(abs_url, src)
                try:
                    all_js_content += f"/* {src} */\n{content.decode('utf-8', errors='ignore')}\n;\n"
                except:
                    pass
        if src and not src.startswith("http"):
            script.decompose()

    # Add the single JS file
    new_js = soup.new_tag("script", src="js/script.js")
    if soup.body:
        soup.body.append(new_js)

    ### DOM MANIPULATIONS ###
    
    # Replace brand name
    for text_node in soup.find_all(string=re.compile("Educavo", re.I)):
        text_node.replace_with(re.sub("Educavo", "EduCadTech", text_node, flags=re.I))
        
    # Remove top bar: Email / Location / Login / Register / Apply Now
    # Looking at template, usually it's in a .topbar-area or similar.
    # We will search for common classes or parents of these texts.
    header = soup.find("header")
    top_bars = soup.find_all(class_=re.compile("toolbar|topbar|top-bar", re.I))
    for tb in top_bars:
        tb.decompose()
        
    # Remove purchase button / Search icon
    search_icons = soup.find_all(class_=re.compile("rs-search|flaticon-search|purchase", re.I))
    for s in search_icons:
        # decompose parent li usually
        p = s.find_parent("li")
        if p: p.decompose()
        else: s.decompose()
        
    cart_icons = soup.find_all(class_=re.compile("cart-inner|fa-shopping-bag|mini-cart", re.I))
    for c in cart_icons:
        c.decompose()
        
    user_icons = soup.find_all(class_=re.compile("user-icon", re.I))
    for u in user_icons:
        u.decompose()
            
    # Fix Navigation Bar to exactly: Home | About | Courses | Verify-Certificate | Contact
    nav_links_dict = {
        "index.html": ("Home", "index.html"),
        "about.html": ("About", "about.html"),
        "courses.html": ("Courses", "courses.html"),
        "verify.html": ("Verify-Certificate", "verify.html"),
        "contact.html": ("Contact", "contact.html")
    }
    
    nav = soup.find("ul", class_="nav-menu")
    if nav:
        nav.clear()
        for page_file, (name, link) in nav_links_dict.items():
            li_class = "current-menu-item" if output_name == page_file else ""
            li = soup.new_tag("li", **{"class": li_class})
            a = soup.new_tag("a", href=link)
            a.string = name
            li.append(a)
            nav.append(li)
            
    # Download and keep original images
    for img in soup.find_all("img"):
        src = img.get("src", "")
        # Handle logos explicitly
        if img.get("alt", "").lower() in ["logo", "educavo logo", "educadtech logo"] or "logo" in src.lower():
            img['src'] = 'images/logo.png'
            img['alt'] = 'EduCadTech Logo'
        elif src and not src.startswith("data:") and src != 'images/logo.png':
            abs_url = urllib.parse.urljoin(BASE_URL, src)
            # Local path maps to the src path if it starts with assets, else keep it
            local_path = src
            if not local_path.startswith("assets/images/") and not local_path.startswith("images/"):
                local_path = "assets/images/" + os.path.basename(local_path)
            
            # Download image
            download_file(abs_url, local_path)
            img['src'] = local_path

    # Remove Footer links sections: Recent Posts, Event, Blog, Contact links
    # Retain: About text, Contact info, Copyright
    footer = soup.find("footer")
    if footer:
        # Remove Recent Posts widget
        title_tags = footer.find_all("h3", class_="widget-title", string=re.compile("Recent Posts", re.I))
        for title in title_tags:
            col = title.find_parent(class_=re.compile("col-"))
            if col: col.decompose()
            
        # Remove Courses widget if necessary (User said "Remove: Recent Posts section, Event / Blog / Contact links list". Usually, people want to keep courses, but let's just stick to the specific removal list)
        
        # Remove Event / Blog / Contact links list usually in copy-right-menu
        copy_menu = footer.find("ul", class_="copy-right-menu")
        if copy_menu:
            copy_menu.decompose()
            
    # Remove Newsletter Section
    newsletter = soup.find(class_=re.compile("rs-newsletter", re.I))
    if newsletter:
        newsletter.decompose()
        
    # Clean up copyright
    copyright_div = soup.find("div", class_="copyright")
    if copyright_div:
        p_tag = copyright_div.find("p")
        if p_tag:
            p_tag.clear()
            p_tag.string = "© " + "2026" + " EduCadTech. All Rights Reserved."

    # Remove template emails/domains
    for a_tag in soup.find_all("a", href=re.compile("rstheme.com", re.I)):
        href = a_tag.get("href", "")
        if href.startswith("mailto:"):
            a_tag['href'] = "mailto:info@EduCadTech.com"
            if a_tag.string: a_tag.string = a_tag.string.replace("support@rstheme.com", "info@EduCadTech.com")
        else:
            a_tag['href'] = "#"
            if a_tag.string: a_tag.string = a_tag.string.replace("RSTheme", "EduCadTech")

    for a_tag in soup.find_all(string=re.compile("support@rstheme.com", re.I)):
        a_tag.replace_with(re.sub("support@rstheme.com", "info@EduCadTech.com", a_tag, flags=re.I))

    # Remove template comments
    for comment in soup.find_all(string=lambda text: isinstance(text, bs4.Comment)):
        if "RsTheme" in comment or "KeenItSolutions" in comment or "Template" in comment:
            comment.extract()
            
    # Add WhatsApp Floating Button
    wa_btn = soup.new_tag("a", href="https://wa.me/919944423978", target="_blank", id="whatsapp-btn", style="position:fixed; bottom:20px; left:20px; z-index:9999; background:#25D366; color:white; padding:10px 15px; border-radius:50px; font-size:24px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);")
    wa_icon = soup.new_tag("i", **{"class": "fa fa-whatsapp"})
    wa_btn.append(wa_icon)
    if soup.body:
        soup.body.append(wa_btn)

    if output_name == "verify.html":
        # Change Breadcrumb Title
        page_title = soup.find("h1", class_="page-title")
        if page_title: page_title.string = "Verify Certificate"
        active_bc = soup.find("a", class_="active")
        if active_bc and active_bc.parent.find_next_sibling("li"):
            active_bc.parent.find_next_sibling("li").string = "Verify Certificate"

        # Find the main contact section and replace it
        contact_section = soup.find("div", class_=re.compile("contact-page-section"))
        if contact_section:
            contact_section.clear()
            # Build the verify certificate form markup
            verify_html = """
            <div class="container pt-100 pb-100">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <div class="rs-quick-contact">
                            <div class="inner-part text-center mb-50">
                                <h2 class="title mb-15">Verify Your Certificate Here...</h2>
                                <p>Submit your Details</p>
                                <br>
                                <h5>Verification mail will be send soon !!</h5>
                            </div>
                            <form id="verify-form" action="" method="post" onsubmit="sendVerifyEmail(event)">
                                <div class="row">
                                    <div class="col-lg-6 mb-35 col-md-12">
                                        <input class="from-control" type="text" id="verify_name" name="name" placeholder="Student Name" required>
                                    </div>
                                    <div class="col-lg-6 mb-35 col-md-12">
                                        <input class="from-control" type="email" id="verify_email" name="email" placeholder="Email Address" required>
                                    </div>
                                    <div class="col-lg-12 mb-35">
                                        <input class="from-control" type="text" id="verify_cert" name="certificate_number" placeholder="Certificate Number" required>
                                    </div>
                                    <div class="col-lg-12 mb-35">
                                        <input class="from-control" type="text" id="verify_course" name="course_name" placeholder="Course Name" required>
                                    </div>
                                </div>
                                <div class="form-group mb-0 text-center">
                                    <button class="readon orange-btn" type="submit">Verify Now</button>
                                </div>
                            </form>
                            <script>
                                function sendVerifyEmail(e) {
                                    e.preventDefault();
                                    const name = document.getElementById('verify_name').value;
                                    const email = document.getElementById('verify_email').value;
                                    const cert = document.getElementById('verify_cert').value;
                                    const course = document.getElementById('verify_course').value;
                                    
                                    const subject = encodeURIComponent(`Certificate Verification Request - ${cert}`);
                                    const body = encodeURIComponent(
                                        `Student Name: ${name}\\n` +
                                        `Email: ${email}\\n` +
                                        `Certificate Number: ${cert}\\n` +
                                        `Course Name: ${course}\\n\\n` +
                                        `Please verify my certificate.`
                                    );
                                    
                                    window.location.href = `mailto:admin@educadtech.com?subject=${subject}&body=${body}`;
                                }
                            </script>
                        </div>
                    </div>
                </div>
            </div>
            """
            contact_section.append(BeautifulSoup(verify_html, "html.parser"))

    with open(output_name, "w", encoding="utf-8") as f:
        f.write(str(soup))

# Post-process CSS to hoist all @import rules to the top
css_imports = []
def extract_imports(match):
    css_imports.append(match.group(0))
    return ""

all_css_content = re.sub(r'@import\s+url\([^\)]+\)\s*;|\@import\s+[\'"][^\'"]+[\'"]\s*;', extract_imports, all_css_content)

# Hoist imports to top
final_css = "\n".join(css_imports) + "\n\n" + all_css_content

# Write combined CSS and JS
with open("css/style.css", "w", encoding="utf-8") as f:
    f.write(final_css)

with open("js/script.js", "w", encoding="utf-8") as f:
    f.write(all_js_content)

print("Build complete.")
