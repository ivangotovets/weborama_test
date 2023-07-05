import sys
import warnings

from ebooklib import epub

EPUB_MAP = {
    'Author':  'creator',
    'Title': 'title',
    'Published by': 'publisher',
    'Date': 'date'
}

warnings.filterwarnings("ignore")
book_name = sys.argv[1]
book = epub.read_epub(book_name)
md = book.metadata['http://purl.org/dc/elements/1.1/']

if book_name.endswith('.epub'):
    for key, value in EPUB_MAP.items():
        print('{}: {}'.format(key, md[value][0][0]))
else:
    print('Неверный формат файла')
