import os
from requests import get 
from bs4 import BeautifulSoup
import pandas as pd

data = []
base_url = "https://www.amazon.in"

def get_products(url):
    req = get(url)
    soup = BeautifulSoup(req.content,'html5lib')
    if req.status_code == 200:
        for tag in soup.findAll("div",attrs={"data-component-type":"s-search-result"}):
            try:
                data.append({"Product URL" : base_url+tag.find('div',attrs={"class":"a-section a-spacing-none puis-padding-right-small s-title-instructions-style"}).a['href'],\
                                    "Product Name":tag.find('span',attrs={"class":"a-size-medium a-color-base a-text-normal"}).text,\
                                    "Product Price":tag.find("span",attrs={"class":"a-price"}).span.text[1:],\
                                    "Rating":tag.find("span",attrs={"class":"a-declarative"}).span.text.split(" ")[0],\
                                    "Number of reviews":tag.find("a",attrs={"href":tag.find('div',attrs={"class":"a-section a-spacing-none puis-padding-right-small s-title-instructions-style"}).a['href']+"#customerReviews"}).text})
            except AttributeError:
                pass
    else:
        get_products(url)

print("Part 1 Started")
for page in range(1,21):
    url = f"https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    # print(f"page : {page}\nURL : {url}") # Debug Purpose
    get_products(url)

pd.DataFrame(data).to_csv(r"part1_data.csv",index=False)

os.system("clear")
print("Part 1 Ended")



print("Part 2 Started")
count=0
for product in data:
    req = get(product["Product URL"])
    while req.status_code != 200:
        req = get(product["Product URL"])

    try:
        soup = BeautifulSoup(req.content,'html5lib')
        product["Description"] = soup.find("meta",attrs={"name":"description"})['content']
        product["ASIN"] = soup.find("input",attrs={"name":"ASIN"})['value']
        product["Manufacturer"] = soup.find("div",attrs={"class":"a-section a-spacing-medium brand-snapshot-flex-row"}).text[3:-2]
        product["Product Description"] = soup.find("meta",attrs={"name":"description"})['content']
        count+=1
        # print(f"Product Count : {count}") # Debug Purpose
    except:
        pass

    if count == 200:
        break
pd.DataFrame(data).dropna().to_csv(r"part2_data.csv",index=False)

print("Part 2 Ended")