import re

target = "d:/Freelancing/Project 2/courses.html"
with open(target, "r", encoding="utf-8") as f:
    html = f.read()

start_str = '<div class="col-lg-4 col-md-6 grid-item filter4 technical mb-30">'
idx = html.find(start_str)
if idx != -1:
    # Insert closing div before the newly added items
    html = html[:idx] + '</div>\n                    ' + html[idx:]
    
    # We also need to remove the extra closing div at the end since we are prepending one.
    # The string we appended before was inserted before:
    # </div>\n                </div>\n            </div>\n        </div>\n        <div class="pagination-area'
    
    # Let's search for 5 closing divs and remove the first one. Actually, wait. 
    # The end structure now looks like:
    # </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class="pagination-area'
    # wait, my appended string ended with `</div>\n                    </div>` which is the item closing div.
    # And it was appended BEFORE the old 4 `</div>`s.
    # So the old 1st `</div>` (which belonged to Primavera) is now immediately following my appended `</div>\n                    </div>`.
    # Let's just find the exact string that is currently there:
    end_frag = '</div>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class="pagination-area'
    # Wait, the appended `out_html` had no exact trailing spaces after its final `</div>`.
    # Let's just use regex to fix the end. 
    # We want to replace 5 consecutive closing `</div>`s with 4.
    
    html = re.sub(r'(</div>\s*){5}<div class="pagination-area', 
                  '</div>\n                </div>\n            </div>\n        </div>\n        <div class="pagination-area', 
                  html, count=1)

    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixed formatting.")
else:
    print("Could not find start str.")
