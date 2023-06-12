import requests
from bs4 import BeautifulSoup
from modules import function

if __name__ == '__main__':

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

    url = r'https://www.amazon.com/s?k=notebook+gamer&i=computers-intl-ship&crid=2MMC2WMSFMH8G&sprefix=note%2Ccomputers-intl-ship%2C191&ref=nb_sb_ss_ts-doa-p_2_4'

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
        product_title.append(function_py.get_title(new_page))
        product_price.append(function_py.get_price(new_page))
        product_rating.append(function_py.get_rating(new_page))
        product_review.append(function_py.get_review(new_page))
        product_available.append(function_py.get_available(new_page))

df_result = function_py.consolidate_results(product_url,
                                            product_title,
                                            product_price,
                                            product_rating,
                                            product_review,
                                            product_available
                                            )

# df_result.to_csv(r'data\result.txt',
#                  sep=';',
#                  encoding='utf8',
#                  index=False,
#                  )