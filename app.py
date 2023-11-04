from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def get_data_from_flipkart(product_name):
    search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name_elem = soup.find('div', class_='_4rR01T')
        price_elem = soup.find('div', class_='_30jeq3')
        img_elem = soup.find('img', class_='_396cs4')
        rating_elem = soup.find('div', class_='_3LWZlK')
        review_counts_elem = soup.find('span', class_='_2_R_DZ')
        
        if product_name_elem:
            product_name = product_name_elem.text.strip()
        else:
            product_name = "N/A"
        
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = "N/A"
        
        if img_elem:
            img_url = img_elem['src']
        else:
            img_url = ""
        
        if rating_elem:
            rating = rating_elem.text.strip()
        else:
            rating = "N/A"
        
        if review_counts_elem:
            review_counts = review_counts_elem.text.strip()
        else:
            review_counts = "N/A"
        
        return {
            "product_name": product_name,
            "price": price,
            "img_url": img_url,
            "rating": rating,
            "review_counts": review_counts
        }
    else:
        return None

def get_data_from_amazon(product_name):
    search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name_elem = soup.find('span', class_='a-text-normal')
        price_elem = soup.find('span', class_='a-price-whole')
        img_elem = soup.find('img', class_='s-image')
        rating_elem = soup.find('span', class_='a-icon-alt')
        review_counts_elem = soup.find('span', class_='a-size-base')
        
        if product_name_elem:
            product_name = product_name_elem.text.strip()
        else:
            product_name = "N/A"
        
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = "N/A"
        
        if img_elem:
            img_url = img_elem['src']
        else:
            img_url = ""
        
        if rating_elem:
            rating = rating_elem.text.strip()
        else:
            rating = "N/A"
        
        if review_counts_elem:
            review_counts = review_counts_elem.text.strip()
        else:
            review_counts = "N/A"
        
        return {
            "product_name": product_name,
            "price": price,
            "img_url": img_url,
            "rating": rating,
            "review_counts": review_counts
        }
    else:
        return None

@app.route('/', methods=['POST', 'GET'])
def home():
    product_data = None

    if request.method == "POST":
        product_name = request.form.get('product_name')
        if product_name:
            amazon_data = get_data_from_amazon(product_name)
            flipkart_data = get_data_from_flipkart(product_name)
            product_data = {"Amazon": amazon_data, "Flipkart": flipkart_data}

    return render_template('index.html', product_data=product_data)

if __name__ == '__main__':
    app.run(debug=True)
