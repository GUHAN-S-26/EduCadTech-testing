from bs4 import BeautifulSoup

target = "d:/Freelancing/Project 2/courses.html"
with open(target, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

courses = soup.find_all("div", class_="courses-item")
for course in courses:
    # 1. remove <span class="price">$55.00</span>
    # The price is usually in <ul class="meta-part"> -> <li> -> <span class="price">
    price_span = course.find("span", class_="price")
    if price_span:
        # remove the parent li if it exists and only contains the price
        parent_li = price_span.parent
        price_span.decompose()
        if parent_li and parent_li.name == "li" and not parent_li.get_text(strip=True):
            parent_li.decompose()

    # 2. remove <a href="#"><i class="flaticon-right-arrow"></i></a>
    # usually inside <div class="btn-part">
    btn_part = course.find("div", class_="btn-part")
    if btn_part:
        arrow_a = btn_part.find("a")
        if arrow_a:
            # check if it has the right arrow or says Apply Now
            icon = arrow_a.find("i", class_="flaticon-right-arrow")
            if icon:
                # remove the entire a tag
                arrow_a.decompose()

    # 3. Add the ratings ul section
    # <div class="info-meta">
    info_meta = course.find("div", class_="info-meta")
    if info_meta:
        # check if it already has the ul
        existing_ul = info_meta.find("ul")
        if not existing_ul:
            # it doesn't have it, let's add it
            # parse the new ul
            new_ul_html = """
                                        <ul>
                                            <li class="user"><i class="fa fa-user"></i> 245</li>
                                            <li class="ratings">
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                (05)
                                            </li>
                                        </ul>"""
            new_ul = BeautifulSoup(new_ul_html, "html.parser").ul
            info_meta.append(new_ul)
            
with open(target, "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Course UI standardized.")
