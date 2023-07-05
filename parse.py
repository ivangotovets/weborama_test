import json
import sys
import warnings
import xmltodict

# пакет сразу под капотом преобразует epub в json
from ebooklib import epub

# перед парсингом открыть подходящим редактором файлы
# для того, чтобы понять, где искать метадату и сделать мэппинг ключей
EPUB_MAP = {
    "Author": "creator",
    "Title": "title",
    "Published by": "publisher",
    "Year": "date",
}

FB2_MAP = {
    "Author": "sequence",
    "Title": "book-name",
    "Published by": "publisher",
    "Year": "year",
}


warnings.filterwarnings("ignore")

# достать название файла из аргумента CLI
book_name = sys.argv[1]

if book_name.endswith(".epub"):
    # сконвертировать epub в json
    book = epub.read_epub(book_name)
    # достать метадату по ключу, если не нашли - перехватить исключение
    try:
        meta = book.metadata["http://purl.org/dc/elements/1.1/"]
    except KeyError:
        print("Метадата о книге отсутствует")
    else:
        # вывести данные согласно мэппингу
        for key, value in EPUB_MAP.items():
            print("{}: {}".format(key, meta[value][0][0]))

elif book_name.endswith(".fb2"):
    with (
        # считать файл как xml побайтно
        open(book_name, "rb") as file_in,
        # метадату удобно анализировать в json в отдельном файле
        # оставил как пример
        open("output.json", "w", encoding="UTF-8") as file_out,
    ):
        lines = file_in.read()
        # сконвертировать xml в json
        data = xmltodict.parse(lines)
        try:
            # достать метадату, если не нашли - перехватить исключение
            meta = data["FictionBook"]["description"]["publish-info"]
        except KeyError:
            print("Метадата о книге отсутствует")
        else:
            # анализировать формат вывода метадаты
            json.dump(data, file_out, ensure_ascii=False, indent=4)
            for key, value in FB2_MAP.items():
                if value == "sequence":
                    # достать автора по отдельному ключу в словаре 'sequence'
                    print("{}: {}".format(key, meta[value]["@name"]))
                else:
                    print("{}: {}".format(key, meta[value]))
else:
    print("Неверный формат файла")
