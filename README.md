# Yatube

### Описание

Yatube - социальная сеть с размещением постов на различные темы.

### Технологии

Python 3.7
Django 2.2.19

### Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndrewYatskevich/yatube.git
```

```
cd yatube/yatube
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python3 manage.py migrate
```

- Запустить проект:

```
python3 manage.py runserver
```

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Автор: Андрей Яцкевич https://github.com/AndrewYatskevich