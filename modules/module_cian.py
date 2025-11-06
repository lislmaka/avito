from bs4 import BeautifulSoup
# import datetime
from .utils import copy_file_to_html_folder, create_images_dir, download_image, trans_ru_en
import re
from .utils import fields_dict
from .module_sqlite import sqlite3_get_fields_names


def parse_cian(fp, file, fnew=False):
    # print(file)
    # # get_file_size()
    data = {}
    soup = BeautifulSoup(fp, "html.parser")

    id = soup.find("meta", {"name": "ca-offer-id"})
    data["id"] = id["content"]

    title = soup.find("meta", property="og:title")
    data["title"] = title["content"]

    address = soup.find("meta", property="og:description")
    data["address"] = address["content"]

    url = soup.find("meta", property="og:url")
    data["url"] = url["content"]

    price = soup.find("div", attrs={"data-testid": "price-amount"}).text
    # data["price"] = price.replace(" ", "").replace("₽", "")
    data["price"] = re.sub(r"[^\d]", "", price)

    # date add
    # data["date_add"] = datetime.date.today().strftime("%d%m%Y")
    data["date_add"] = None
    data["date_update"] = None

    # etazh
    _, etazh = data["title"].rsplit(maxsplit=1)
    etazh_val, etazh_count = etazh.split("/")
    data["etazh_val"] = etazh_val
    data["etazh_count"] = etazh_count
    data["etazh"] = f"{etazh_val} из {etazh_count}"

    # kolichestvo_komnat
    kk, _ = data["title"].split("-", maxsplit=1)
    _, kolichestvo_komnat = kk.split()
    data["kolichestvo_komnat"] = kolichestvo_komnat

    params = soup.find_all("div", attrs={"data-name": "OfferSummaryInfoItem"})
    for param in params:
        ps = param.find_all("p")
        f_key = trans_ru_en(ps[0].text)
        f_value = ps[1].text
        fields = fields_dict()
        sqlite_fields = sqlite3_get_fields_names()

        if f_key not in sqlite_fields:
            key = [k for k, v in fields.items() if f_key in v]
            if not key: 
                print(f"---> {f_key} ({ps[0].text}) not in fields list") 
            else:
                data[key] = f_value
        else:
            data[f_key] = f_value

    if fnew:
        span_img = soup.find("div", attrs={"data-name": "GalleryInnerComponent"})
        img = span_img.find("img")
        print(img["src"])
        copy_file_to_html_folder(data["id"], "cian")
        create_images_dir(data["id"])
        download_image(url=img["src"], id=data["id"])
        
    data["obshchaya_ploshchad"] = re.sub(r"[^\d\,]", "", data["obshchaya_ploshchad"]).replace(",", ".")
    data["ploshchad_kukhni"] = re.sub(r"[^\d\,]", "", data["ploshchad_kukhni"]).replace(",", ".")
    data["zhilaya_ploshchad"] = re.sub(r"[^\d\,]", "", data["zhilaya_ploshchad"]).replace(",", ".")
    # print(data)
    # exit()

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
    data["lift_diff"] = None
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
    data["is_neighbors_around"] = None
    data["is_neighbors_top"] = None
    data["is_door"] = None

    data["record_status"] = 1

    data["door"] = None
    data["kuxnya"] = None
    data["tualet"] = None
    data["vana"] = None
    data["balkon"] = None
    data["to_bus_stop"] = None
    data["gkx_payments"] = None
    data["neighbors_around"] = None
    data["neighbors_top"] = None
    data["tambur"] = None
    data["no_stupenki"] = None
    data["musoroprovod"] = None
    
    data["status"] = 1
    data["source_from"] = "cian"

    return data
