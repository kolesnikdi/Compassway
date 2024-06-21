# weather_scraping
## Використані інструменти:
- Контейнеризація: Docker, Docker-compose
- Основний фреймвок: Django, DRF
- БД: PostgreSQL (основна), Redis (broker)
- Скрапінг сайту: BeautifulSoup
- Задачі за розкладом: Celery
- Автотестування: Pytest
- Адміністрування БД: adminer

## Додаткові пояснення
- Сайт для парсинга: https://pogoda.meta.ua/ було змінено на https://ua.sinoptik.ua/
- Для автоматичного оновлення існуючих записів в БД використовується bulk.
- За скрапінг і запит до сайту відповідає клас WeatherScraping.

## Запуск проекту 
- git clone https://github.com/kolesnikdi/dZENcode.git
- cd .\Compassway\weather_scraping
- Скопіюй .env файл до \Compassway\weather_scraping
- python manage.py createsuperuser
- docker-compose up --build
- Запуск end-to-end тестів. Термінал Docker -> weather_scraping -> web-1 `pytest`


## Endpoints
### Негайний запит і скрапінг сайту
-  [update_weather](http://127.0.0.1:8000/weather/update/) 
Повертає дані за поточну дату +5 днів вперед.
### Перегляд останніх 6 записів про погоду
- Звичайне відображення.
[WeatherView](http://127.0.0.1:8000/weather/)
- Відображення через адмін панель.
[WeatherAdmin](http://127.0.0.1:8000/admin/weather/)
### Зміна часу виконання запиту і скрапінгу сайту.
- [UpdateTimeView](http://127.0.0.1:8000/weather/time_update/)
### Перегляд завдвнь які виконуються.
- Черга.
[Scheduled](http://127.0.0.1:8000/admin/django_celery_beat/periodictask/)
- Стан виконання.
[In Progress, Done](http://127.0.0.1:8000/admin/django_celery_results/taskresult/)
### Інші посилання
[adminer](http://127.0.0.1:8082) Логін та Пароль в файлі .env
