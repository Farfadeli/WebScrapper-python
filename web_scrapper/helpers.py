import requests
from bs4 import BeautifulSoup

def get_all_page_url(page):
    nb = page.select("form strong")
    rep = [e.string for e in nb]
    nb_pages = int(rep[0]) // 20
    res = ["https://books.toscrape.com/"]
    [res.append(res[0] + f"catalogue/page-{e}.html") for e in range(2, nb_pages+1)]
    return res

def get_all_links(url: str):
    request = requests.get(url)
    content = request.content
    page = BeautifulSoup(content, 'html.parser')
    data = page.select(".product_pod h3 a")
    print("ahah")
    return ["https://books.toscrape.com/"+e["href"] if "catalogue" in e["href"] else "https://books.toscrape.com/catalogue/"+e["href"] for e in data]

def tab_array(page: BeautifulSoup):
    rep = page.select("table tr td")
    return [i.string for i in rep]

def get_num_available(elem: str):
    rep = ""
    for e in elem:
        if e.isnumeric():
            rep += e
    return int(rep)

def get_image(page: BeautifulSoup):
    data = page.select(".thumbnail .carousel-inner .item img")[0]["src"]
    data = data.replace("../../", "https://books.toscrape.com/")
    return data

def get_rating(page: BeautifulSoup):
    match page.select(".product_main .star-rating")[0]["class"][1]:
        case "One": return 1
        case "Two" : return 2
        case "Three" : return 3
        case "Four" : return 4
        case "Five" : return 5
        case _: return 0

def get_home_page():
    url = "https://books.toscrape.com/"
    request = requests.get(url)

    content = request.content

    return BeautifulSoup(content, 'html.parser')