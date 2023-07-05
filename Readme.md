## Как запустить проект
### Клонировать репозиторий и перейти в него в командной строке:

`git clone git@github.com:ivangotovets/weborama_test.git`

`cd Weborama_test`

### Cоздать и активировать виртуальное окружение:

`python3 -m venv venv`

`source venv/bin/activate`

### Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

### Задание 1 - см. файл Jupiter Notebook "task_1.ipynb"

### Задание 2 - запуск парсера:

`python parse.py 'TRANSHUMANISM.epub'`
`python parse.py 'КГБТ.epub'`
`python parse.py 'TRANSHUMANISM.fb2'`
`python parse.py 'КГБТ.fb2'`


