import json
import sys
import warnings
import xmltodict

# пакет сразу под капотом преобразует epub в json
from ebooklib import epub

# перед парсингом открыть подходящим редактором файлы
# для того, чтобы понять, где искать метадату, сделать мэппинг индексов
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
    book = epub.read_epub(book_name)
    # достать метадату в json, если не нашли - перехватить исключение
    try:
        meta = book.metadata["http://purl.org/dc/elements/1.1/"]
    except KeyError:
        print("Метадата о книге отсутствует")
    else:
        # вывести данные согласно мэппингу
        for field, index in EPUB_MAP.items():
            data = meta.get(index)
            if data:
                print("{}: {}".format(field, data[0][0]))

elif book_name.endswith(".fb2"):
    with (
        # считать файл как xml побайтно
        open(book_name, "rb") as file_in,
        # целую книгу удобно анализировать в json в отдельном файле
        open("output_fb2.json", "w", encoding="UTF-8") as file_out,
    ):
        lines = file_in.read()
        # сконвертировать xml в json
        data = xmltodict.parse(lines)
        # файл для анализа
        json.dump(data, file_out, ensure_ascii=False, indent=4)
        try:
            # достать метадату, если не нашли - перехватить исключение
            meta = data["FictionBook"]["description"]["publish-info"]
        except KeyError:
            print("Метадата о книге отсутствует")
        else:
            for field, index in FB2_MAP.items():
                data = meta.get(index)
                if data:
                    if index == "sequence":
                        # достать автора по ключу из отдельного словаря
                        print("{}: {}".format(field, data.get("@name", "")))
                    else:
                        print("{}: {}".format(field, data))
else:
    print("Неверный формат файла")
