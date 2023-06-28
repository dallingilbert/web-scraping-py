# web scraping example using Beautiful Soup
from urllib.request import urlopen
from bs4 import BeautifulSoup

# open url
url = "http://olympus.realpython.org/profiles"
page = urlopen(url)
html = page.read().decode("utf-8")

# create soup object
soup = BeautifulSoup(html, "html.parser")

# store each link in a seperate var
a_tag1, a_tag2, a_tag3 = soup.find_all("a")

# concatenate strings to create a url
base_url = "http://olympus.realpython.org"
print(base_url + a_tag1["href"])
print(base_url + a_tag2["href"])
print(base_url + a_tag3["href"])