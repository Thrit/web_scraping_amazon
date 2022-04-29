import re
import pandas as pd

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find('span', attrs={'id': 'productTitle'}).string.strip()
    except AttributeError:
        title = ''
    return title


# Function to extract Product Price
def get_price(soup):

    regex = r'^R\$|\$|€$'

    try:
        price = soup.find('span', attrs={'class': 'a-size-base a-color-base'}).string.strip()
        if not bool(re.search(regex, price)):
            price = soup.find('span', attrs={'class': 'a-color-price a-text-bold'}).string.strip().replace('From ', '')
    except AttributeError:
        price = ''
    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find('i', attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        rating = ''
    return rating


# Function to extract Number of User Reviews
def get_review(soup):
    try:
        review = soup.find('span', attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review = ''
    return review


# Function to extract Availability Status
def get_available(soup):
    try:
        available = soup.find('div', attrs={'id': 'availability'}).find("span").string.strip()
    except AttributeError:
        available = ''
    return available

def consolidate_results(product_url,
                        product_title,
                        product_price,
                        product_rating,
                        product_review,
                        product_available
                        ):
    data = {
        'product_url': product_url,
        'product_title': product_title,
        'product_price': product_price,
        'product_rating': product_rating,
        'product_review': product_review,
        'product_available': product_available
    }

    return pd.DataFrame(data)
