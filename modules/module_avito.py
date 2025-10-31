from bs4 import BeautifulSoup
# import datetime
from .utils import trans_ru_en


def parse_avito(fp):
    data = {}
    soup = BeautifulSoup(fp, "html.parser")

    url = soup.find("meta", property="og:url")
    data["url"] = url["content"]
    _, id = soup.find(attrs={"data-marker": "item-view/item-id"}).text.split()
    data["id"] = id.strip()
    # date_site = soup.find(attrs={"data-marker": "item-view/item-date"}).text
    # data["date_site"] = date_site.strip()
    data["date_add"] = None
    data["date_update"] = None
    data["title"] = soup.find(attrs={"data-marker": "item-view/title-info"}).text
    # *price, _ = soup.find(attrs={"data-marker": "item-view/item-price"}).text.split()
    # data["price"] = "".join(price)
    price = soup.find("meta", property="product:price:amount")
    data["price"] = price["content"]

    try:
        address = soup.find("span", class_="style__item-address__string___XzQ5MT")
        data["address"] = address.text
    except Exception:
        try:
            address = soup.find("span", class_="xLPJ6")
            data["address"] = address.text
        except Exception:
            data["address"] = None

    # try:
    #     data["seller"] = soup.find(attrs={"data-marker": "seller-info/name"}).text
    # except Exception:
    #     pass
    seller = soup.find("meta", property="vk:seller_name")
    data["seller"] = seller["content"]

    params = soup.find_all(attrs={"data-marker": "item-view/item-params"})
    for param in params:
        for p in param.find_all("li"):
            k, v = p.text.split(":")
            data[trans_ru_en(k.strip())] = v.strip()

    val, _ = data["obshchaya_ploshchad"].split()
    data["obshchaya_ploshchad"] = val

    val, _ = data["ploshchad_kukhni"].split()
    data["ploshchad_kukhni"] = val

    etazh_val, etazh_count = data["etazh"].split("из")
    data["etazh_val"] = etazh_val.strip()
    data["etazh_count"] = etazh_count.strip()

    data["to_magazin"] = None
    data["to_pyaterochka"] = None
    data["to_magnit"] = None
    data["to_bolnitsa"] = None
    data["to_pochta"] = None
    data["to_bank"] = None
    data["to_apteka"] = None
    data["to_ozon"] = None
    data["to_wildberries"] = None
    data["to_yandex"] = None
    data["status"] = "Активное"
    data["source_from"] = "avito"
    data["kapremont_date"] = None

    try:
        val, _ = data["zhilaya_ploshchad"].split()
        data["zhilaya_ploshchad"] = val
    except Exception:
        pass

    return data
