import requests
from bs4 import BeautifulSoup
from collections import namedtuple


def produce_ebay_prices() -> None:
    """Asks for parameters for an item and produces details for it"""

    base_url = "https://www.ebay.com/sch/"
    payload = dict()

    payload = _get_url_params(payload)
    source = _get_url_source(base_url, payload)
    item_list = _get_source_details(source)

    return


def _get_source_details(source: requests) -> list[namedtuple]:
    """Gets the details from the html source provided and returns a list of the details"""

    item_list = []
    item_details = namedtuple("item_details", ["title", "price", "time"])
    prices_list = []
    time_list = []
    title_list = []

    soup = BeautifulSoup(source.text, features="html.parser")
    prices = soup.find_all(class_="s-item__price")
    times = soup.find_all(class_="s-item__listingDate")
    titles = soup.find_all(class_="s-item__title")

    for elements in prices:
        price = elements.find(string=True)
        prices_list.append(price)

    for elements in times:
        time = elements.find(string=True)
        time_list.append(time)

    for elements in titles:
        title = elements.find_all(string=True)

        if not title:
            continue

        title = ' '.join(title)
        title_list.append(title)

    for index in range(len(prices_list)):
        item_list.append(item_details(title=title_list[index], price=prices_list[index], time=time_list[index]))

    return item_list


def _get_url_params(payload: dict) -> dict:
    """Fills up a payload dictionary with search parameters and values"""

    while True:
        param1 = input("Please enter search parameter (_sop, _nkw) (Press Enter to quit): ")
        if param1 == "":
            break

        param2 = input("Please enter search parameter value (10, keywords) (Press Enter to quit): ")
        if param2 == "":
            break

        payload.update({param1: param2})

    return payload


def _get_url_source(base_url: str, payload: dict) -> requests:
    """Takes a url string as input and returns the html source code"""

    source = requests.get(base_url, params=payload)
    return source


if __name__ == '__main__':
    produce_ebay_prices()
