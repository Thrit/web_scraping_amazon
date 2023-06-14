import os
import requests
import pandas as pd

from typing import ClassVar
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(dotenv_path='.env')


def get_data_from_url(url: str) -> None:

    product_url = []
    product_title = []
    product_price = []
    product_rating = []
    product_amount_ratings = []
    product_availability = []

    headers = (
        {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept-Language': 'en-US'
        }
    )

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    links = soup.find_all('a', attrs={'class': 'a-link-normal s-no-outline'})
    link_subdirectory = []

    for link in links:
        link_subdirectory.append(link.get('href'))

    for subdirectory in link_subdirectory:

        url_full = 'https://www.amazon.com{subdirectory}'
        item_page = requests.get(url_full.format(subdirectory=subdirectory), headers=headers, timeout=5)
        item_page.close()

        item_attributes = BeautifulSoup(item_page.content, 'lxml')

        product_url.append(url_full.format(subdirectory=subdirectory))
        product_title.append(get_title(item_attributes))
        product_price.append(get_price(item_attributes))
        product_rating.append(get_rating(item_attributes))
        product_amount_ratings.append(get_amount_ratings(item_attributes))
        product_availability.append(get_availability(item_attributes))

    df_result = consolidate_results(
        product_url,
        product_title,
        product_price,
        product_rating,
        product_amount_ratings,
        product_availability
    )

    engine_url = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(engine_url)
    df_result.to_sql('amazon_data', engine)


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
        return soup.find('span', attrs={'class': 'a-offscreen'}).string.strip()
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
        return soup.find('span', attrs={'id': 'acrPopover'})['title']
    except TypeError:
        return ''


def get_amount_ratings(soup: ClassVar) -> str:
    """
    Extract the amount of ratings made in the product.

    Attributes
    ----------
        soup: BeautifulSoap Object.
    """

    try:
        return soup.find('span', attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        return ''


def get_availability(soup: ClassVar) -> str:
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
        product_amount_ratings: list,
        product_availability: list
) -> object:
    """
    Consolidate all the lists into a dataframe.

    Attributes
    ----------
        product_url: List of items and their URLs,
        product_title: List of titles from each URL,
        product_price: List of prices from each URL,
        product_rating: List of rating from each URL,
        product_amount_ratings: List of the amount of ratings from each URL,
        product_availability: List of availability from each URL
    """

    data = {
        'product_url': product_url,
        'product_title': product_title,
        'product_price': product_price,
        'product_rating': product_rating,
        'product_amount_ratings': product_amount_ratings,
        'product_availability': product_availability
    }

    return pd.DataFrame(data)
