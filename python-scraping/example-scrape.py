# Write a program that grabs the full HTML from the following URL
import re
from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")

h2_start = html.find("<h2>") + len("<h2>")
h2_end = html.find("</h2>")

h2_tag = html[h2_start:h2_end]

print(f"This is the name: {h2_tag}")
print(html)
