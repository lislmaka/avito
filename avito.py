from modules.utils import get_raw_files, get_file_size
from modules.module_avito import parse_avito
from modules.module_cian import parse_cian
from modules.module_sqlite import (
    sqlite3_get_fields_names,
    sqlite3_add_new_field,
    sqlite3_add_new_values,
)
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def main(site_name=None):
    for file in get_raw_files():
        with open(f"{os.environ.get('AVITO_PATH_FILES')}/{file}") as fp:
            if file.startswith("avito"):
                data = parse_avito(fp, file, fnew=False)
            elif file.startswith("cian"):
                data = parse_cian(fp, file, fnew=False)
                pass
            elif file.startswith("new"):
                if get_file_size():
                    if site_name == "avito":
                        data = parse_avito(fp, file, fnew=True)
                    elif site_name == "cian":
                        data = parse_cian(fp, file, fnew=True)
                    else:
                        pass
            else:
                print(f"Неправильное название файла - {file}")
                continue

            for field, value in data.items():
                sqlite_fields = sqlite3_get_fields_names()
                if field not in sqlite_fields:
                    sqlite3_add_new_field(field)
            status = sqlite3_add_new_values(data)
            print(f"File {file}, params ({len(data)}), operation ({status.upper()})")


if __name__ == "__main__":
    site_name = None
    if len(sys.argv) == 2:
        site_name = sys.argv[1]
    main(site_name)
