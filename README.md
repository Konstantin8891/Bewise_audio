# Bewise_audio

Сервис для конвертации и хранения mp3 в wav 

## Пререквизиты

На компьютере должен быть установлен Docker

## Стек

FastAPI

PostgreSQL

pydub

## Запуск проекта

git clone git@github.com:Konstantin8891/Bewise_audio.git

cd Bewise_audio

cd backend

nano .env

содержание .env файла:

POSTGRES_DB=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

HOST=db

cd ..

cd infra_audio

docker-compose up --build -d

docker-compose exec backend alembic upgrade head

## Примеры запросов

### Создание пользователя

POST http://localhost:8000/users/create_user

Запрос:

{

    "name": "user5"
    
}

Ответ:

[

    6,
    
    "b4f762e1-7cae-4252-9aae-6e3d049cffb6"
    
]

### Добавление аудиозаписи wav и конвертация в mp3

POST http://localhost:8000/create_audio?user_id=6&uuid=b4f762e1-7cae-4252-9aae-6e3d049cffb6

Где uuid - второй элемент массива из предыдущего запроса, user_id - первый элемент массива из предыдущего запроса

Необходимо отправить аудиозапись (тестовая аудиозапись находится в корне проекта) например с помощью Postman -> Body -> form-data -> Key -> Audio -> тип file -> value выбрать файл

Ответ:

"http://localhost:8000/record?id=3020b54b-fcc9-4999-b6d1-57376c5ceb5f&user=6" - ссылка для скачивания

### Скачивание записи mp3

GET http://localhost:8000/record?id=3020b54b-fcc9-4999-b6d1-57376c5ceb5f&user=6

Где id - uuid аудио записи, user - id пользователя

Ответ:

Файл
