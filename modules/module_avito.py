from bs4 import BeautifulSoup

# import datetime
from .utils import (
    trans_ru_en,
    copy_file_to_html_folder,
    create_images_dir,
    download_image,
    get_file_size,
)


def parse_avito(fp, file, fnew=False):
    # print(file)
    # # get_file_size()
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

    if fnew:
        span_img = soup.find("div", class_="image-frame__wrapper___XzcwYj")
        img = span_img.find("img")
        copy_file_to_html_folder(data["id"], "avito")
        create_images_dir(data["id"])
        download_image(url=img["src"], id=data["id"])

    try:
        address = soup.find("span", class_="style__item-address__string___XzQ5MT")
        data["address"] = address.text
    except Exception:
        try:
            address = soup.find("span", class_="xLPJ6")
            data["address"] = address.text
        except Exception:
            data["address"] = None

    try:
        district = soup.find("span", class_="style__item-address-georeferences-item___XzQ5MT")
        _, district = district.text.split()
        data["district"] = district
    except Exception:
        data["district"] = None
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

    data["tip_doma"] = data["tip_doma"].lower()

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
    data["kapremont_date"] = None
    data["kapremont_diff"] = None
    data["lift_date"] = None
    data["rating"] = None
    data["description"] = None
    data["description_minus"] = None
    data["rating_infrastructure"] = None
    data["rating_house"] = None
    data["rating_flat"] = None
    data["rating_all"] = None
    data["review_results"] = 1

    data["is_kapremont"] = None
    data["is_no_stupenki"] = None
    data["is_musoroprovod"] = None
    data["is_new_lift"] = None

    data["is_kuxnya"] = None
    data["is_tualet"] = None
    data["is_vana"] = None
    data["is_balkon"] = None

    data["record_status"] = 1

    data["status"] = 1
    data["source_from"] = "avito"
    

    try:
        val, _ = data["zhilaya_ploshchad"].split()
        data["zhilaya_ploshchad"] = val
    except Exception:
        pass

    return data
