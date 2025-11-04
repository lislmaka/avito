import os
import shutil
import requests


def get_file_size():
    f_size = os.path.getsize("html/new.txt")
    return f_size


def copy_file_to_html_folder(id, web_source):
    shutil.copy("html/new.txt", f"html/{web_source}_{id}.html")
    open('html/new.txt', 'w').close()

def create_images_dir(id):
    path = os.environ.get("FILE_FOLDER_IMAGES") + f"/{id}"
    if not os.path.isdir(path):
        os.makedirs(path)


def download_image(url, id):
    path = os.environ.get("FILE_FOLDER_IMAGES") + f"/{id}/" + "main.jpg"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    f = open(path, "wb")
    f.write(response.content)
    f.close()


def fields_dict():
    data = {}

    return data


def get_raw_files():
    """Получение списка файлов"""
    path = "html"
    dir_list = os.listdir(path)
    return dir_list


def trans_ru_en(s):
    s = s.lower()
    translit_dict = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "Zh",
        "З": "Z",
        "И": "I",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Shch",
        "Ъ": "",
        "Ы": "Y",
        "Ь": "",
        "Э": "E",
        "Ю": "Yu",
        "Я": "Ya",
        " ": "_",
        "№": "No",
        ",": ",",
        ".": ".",
        "?": "?",
        "!": "!",
        ":": ":",
        ";": ";",
        "-": "-",
        "_": "_",
    }

    return s.translate(s.maketrans(translit_dict))
