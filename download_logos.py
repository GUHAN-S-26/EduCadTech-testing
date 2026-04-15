import urllib.request
import os

os.makedirs('images', exist_ok=True)

url_dark = 'https://keenitsolutions.com/products/html/educavo/assets/images/dark-logo.png'
url_lite = 'https://keenitsolutions.com/products/html/educavo/assets/images/lite-logo.png'

urllib.request.urlretrieve(url_dark, 'images/dark-logo.png')
urllib.request.urlretrieve(url_lite, 'images/lite-logo.png')

print("Logos downloaded successfully.")
