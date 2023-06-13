import re
import requests
import pandas as pd

from bs4 import BeautifulSoup
from typing import ClassVar


def get_data_from_url(url: str) -> object:

    product_url = []
    product_title = []
    product_price = []
    product_rating = []
    product_review = []
    product_available = []

    headers = (
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept-Language': 'en-US'
        }
    )

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    links = soup.find_all('a', attrs={'class': 'a-link-normal s-no-outline'})
    links_list = []

    for link in links:
        links_list.append(link.get('href'))

    for link in links_list:

        url_full = 'https://www.amazon.com{link}'
        new_page = requests.get(url_full.format(link=link), headers=headers)

        new_page = BeautifulSoup(new_page.content, 'lxml')

        product_url.append(url_full.format(link=link))
        product_title.append(get_title(new_page))
        product_price.append(get_price(new_page))
        product_rating.append(get_rating(new_page))
        product_review.append(get_review(new_page))
        product_available.append(get_available(new_page))

        return consolidate_results(
            product_url,
            product_title,
            product_price,
            product_rating,
            product_review,
            product_available
        )


def get_title(soup: ClassVar) -> str:
    """
    Extract the product title.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        return soup.find('span', attrs={'id': 'productTitle'}).string.strip()
    except AttributeError:
        return ''


def get_price(soup: ClassVar) -> str:
    """
    Extract the price value.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        price = soup.find('span', attrs={'class': 'a-size-base a-color-base'}).string.strip()
        if not bool(re.search(r'^R\$|\$|€$', price)):
            return soup.find('span', attrs={'class': 'a-color-price a-text-bold'}).string.strip().replace('From ', '')
    except AttributeError:
        return ''


def get_rating(soup: ClassVar) -> str:
    """
    Extract the product rating value.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        return soup.find('i', attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        return ''


def get_review(soup: ClassVar) -> str:
    """
    Extract the review made in the product.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        return soup.find('span', attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        return ''


def get_available(soup: ClassVar) -> str:
    """
    Extract the availability information of the product.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        return soup.find('div', attrs={'id': 'availability'}).find("span").string.strip()
    except AttributeError:
        return ''


def consolidate_results(
        product_url: list,
        product_title: list,
        product_price: list,
        product_rating: list,
        product_review: list,
        product_available: list
) -> object:
    """
    Consolidate all the lists into a dataframe.

    Attributes
    ----------
        product_url: List of items and their URLs,
        product_title: List of titles from each url,
        product_price: List of prices from each url,
        product_rating: List of rating from each url,
        product_review: List of reviews from each url,
        product_available: List of availability from each url
    """

    data = {
        'product_url': product_url,
        'product_title': product_title,
        'product_price': product_price,
        'product_rating': product_rating,
        'product_review': product_review,
        'product_available': product_available
    }

    return pd.DataFrame(data)
