import requests
from bs4 import BeautifulSoup
from collections import namedtuple


def produce_ebay_prices(payload: dict) -> namedtuple:
    """Asks for parameters for an item on ebay and produces details for it"""

    base_url = "https://www.ebay.com/sch/"

    source = _get_url_source(base_url, payload)
    item_list = _get_source_details(source)

    return item_list


def _get_source_details(source: requests) -> list[namedtuple]:
    """Gets the details from the html source provided and returns a list of the details"""

    item_list = []
    item_details = namedtuple("item_details", ["title", "price", "time", "image", "link"])
    prices_list = []
    time_list = []
    title_list = []
    image_list = []
    link_list = []

    soup = BeautifulSoup(source.text, features="html.parser")

    times = soup.find_all(class_="s-item__listingDate")
    titles = soup.find_all(class_="s-item__title")

    listings = soup.find_all('li', class_="s-item")

    for listing in listings:

        item_name_details = listing.find(class_="s-item__title")
        item_name = str(item_name_details.find(string=True))

        if item_name != "None":
            # Handling with prices -- START
            price_detail = listing.find('span', class_="s-item__price")
            price = price_detail.find(string=True)

            bid = "None"
            bid_detail = listing.find('span', class_="s-item__bids")

            if str(bid_detail) != "None":
                bid = str(bid_detail.find(string=True))

            if bid != "None":
                prices_list.append(price + " current bid")
            else:
                prices_list.append(price)
            # Handling with prices -- END

            # Handling with images -- START
            image_detail = listing.find('img', class_="s-item__image-img")
            image = image_detail['src']

            image_list.append(image)
            # Handling with images -- END

            # Handling with links -- START
            link_detail = listing.find('a', tabindex="-1")
            link = link_detail['href']

            link_list.append(link)
            # Handling with links -- END
        continue

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
        if len(time_list) != len(prices_list):
            item_list.append(item_details(title=title_list[index], price=prices_list[index],
                                          time=0, image=image_list[index], link=link_list[index]))
        else:
            item_list.append(item_details(title=title_list[index], price=prices_list[index],
                                          time=time_list[index], image=image_list[index], link=link_list[index]))

    return item_list


def _get_url_source(base_url: str, payload: dict) -> requests:
    """Takes a url string as input and returns the html source code"""

    source = requests.get(base_url, params=payload)
    return source
