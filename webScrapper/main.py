import os
import requests
import concurrent.futures
from bs4 import BeautifulSoup
import csv
import shutil

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

def book_data(url: str):
    req = requests.get(url)
    content = req.content
    page = BeautifulSoup(content, 'html.parser')
    
    table = tab_array(page)
    upc = table[0].string
    price_exc_tax = float(table[2].string.replace("£", ""))
    price_tax = float(table[3].string.replace("£", ""))
    num_available = get_num_available(table[5])
    img_url = get_image(page)
    title = page.select(".product_main h1")[0].string
    genre = page.select(".breadcrumb li:nth-child(3) a")[0].string.replace(" ", "_")
    describe = page.select("div article p:nth-child(3)")
    describe = "" if len(describe) in [0,1] else describe[1].string
    rating = get_rating(page)
    
    #print(str(os.path.exists("../data/csv/tat.py")))
    if(os.path.exists(f"../data/csv/{genre}.csv") == False):
        with open(f"../data/csv/{genre}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            row = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
            writer.writerow(row)
            
    with open(f"../data/csv/{genre}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            row = [url, upc, title, price_tax, price_exc_tax, num_available, describe, genre, rating, img_url]
            writer.writerow(row)
    
    res_img_book = requests.get(img_url, stream=True)
        
    if(res_img_book.status_code == 200):
        with open(f"../data/img/{genre}_{upc}.jpg", "wb") as img_file:
            shutil.copyfileobj(res_img_book.raw, img_file)
        print("Success import image")
    
    print(f"Success : {title}")
    
def get_books_data(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executer:
        return list(executer.map(book_data, urls))

url = "https://books.toscrape.com/"
request = requests.get(url)

content = request.content

page = BeautifulSoup(content, 'html.parser')

pages_url = get_all_page_url(page)

with concurrent.futures.ThreadPoolExecutor(max_workers=len(pages_url)) as workers:
    results = list(workers.map(get_all_links, pages_url))
    book_array = list(workers.map(get_books_data, results))

