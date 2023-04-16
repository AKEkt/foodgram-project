# Сайт Foodgram
## Описание проекта
    Проект — сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для 
    него. На этом сервисе пользователи смогут публиковать рецепты, подписываться 
    на публикации других пользователей, добавлять понравившиеся рецепты в список 
    «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
    необходимых для приготовления одного или нескольких выбранных блюд.
# ![example workflow](https://github.com/AKEkt/foodgram_project_react/actions/workflows/main.yml/badge.svg)

## Шаблон наполнения env-файла:
	
	DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
	DB_NAME=postgres # имя базы данных
	POSTGRES_USER=postgres # логин для подключения к базе данных
	POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
	DB_HOST=db # название сервиса (контейнера)
	DB_PORT=5432 # порт для подключения к БД 
	

## Команды для запуска приложения в контейнерах

- Установить Docker и Docker Compose https://docs.docker.com/compose/install/:
```
sudo apt install docker-ce docker-compose -y
```
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:AKEkt/foodgram-project-react.git
```
- Перейти в директорию /infra
```
cd infra
```
- Создать файл .env с переменными окружения
```
sudo nano .env
```
- Развёрнуть контейнеры в «фоновом режиме» командой:
```
sudo docker-compose up -d --build
```
- Убедится что контейнеры запущены:
```
sudo docker stats 
```
- В контейнере web выполнить миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```
- Создать суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
- Собрать статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input 
```
- Убедится что приложение становится доступным по адресу http://85.208.208.227/admin/ и статика подгрузилась
- Войти в админку создать одну-две записи объектов или загрузить тестовые данные из dump.json
- Файл dump.json сохранится в директорию /infra
- Узнать CONTAINER ID для образа infra_backend:
```
sudo docker container ls -a
```
- Скопировать файл "dump.json" в контейнер:
```
sudo docker cp dump.json <CONTAINER ID>:/app
sudo docker-compose exec backend python manage.py loaddata dump.json
```
- Протестировать приложение через Postman
```
GET /api/users/
```
- Создать дамп (резервную копию) базы данных:
```
sudo docker-compose exec backend python manage.py dumpdata > fixtures.json
```

