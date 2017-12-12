from bs4 import BeautifulSoup
import requests

def get_soup(url):
    try:
        source_code = requests.get(url)
    except:
        return None
    html = source_code.text
    soup = BeautifulSoup(html,"lxml")
    return soup