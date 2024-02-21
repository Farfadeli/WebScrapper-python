import os
import requests
import concurrent.futures
from bs4 import BeautifulSoup
import csv
import shutil
import helpers

def book_data(url: str):
    req = requests.get(url)
    content = req.content
    page = BeautifulSoup(content, 'html.parser')
    
    table = helpers.tab_array(page)
    upc = table[0].string
    price_exc_tax = float(table[2].string.replace("£", ""))
    price_tax = float(table[3].string.replace("£", ""))
    num_available = helpers.get_num_available(table[5])
    img_url = helpers.get_image(page)
    title = f"""{page.select(".product_main h1")[0].string}"""
    genre = page.select(".breadcrumb li:nth-child(3) a")[0].string.replace(" ", "_")
    describe = page.select("div article p:nth-child(3)")
    describe = "" if len(describe) in [0,1] else describe[1].string
    rating = helpers.get_rating(page)
    
    #print(str(os.path.exists("../data/csv/tat.py")))
    if(os.path.exists(f"./data/csv/{genre}.csv") == False):
        with open(f"./data/csv/{genre}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            row = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
            writer.writerow(row)
            
    with open(f"./data/csv/{genre}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            row = [url, upc, title, price_tax, price_exc_tax, num_available, describe, genre, rating, img_url]
            writer.writerow(row)
    
    res_img_book = requests.get(img_url, stream=True)
        
    if(res_img_book.status_code == 200):
        with open(f"./data/img/{genre}_{upc}.jpg", "wb") as img_file:
            shutil.copyfileobj(res_img_book.raw, img_file)
        print("Success import image")
    
    print(f"Success : {title}")
    
def get_books_data(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executer:
        return list(executer.map(book_data, urls))



with concurrent.futures.ThreadPoolExecutor(max_workers=len(helpers.get_all_page_url(helpers.get_home_page()))) as workers:
    results = list(workers.map(helpers.get_all_links, helpers.get_all_page_url(helpers.get_home_page())))
    book_array = list(workers.map(get_books_data, results))

