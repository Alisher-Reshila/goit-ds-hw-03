import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return "Ошибка: JSON файл не найден."
        except PyMongoError as e:
            return f" Ошибка MongoDB:{e}"
    return inner

@input_error
def upload_data(conect):
    client = MongoClient(conect)
    db = client["quotes_database"]

    with open('authors.json', 'r', encoding='utf-8') as f:
        db.authors.insert_many(json.load(f))
    
    with open('quotes.json', 'r', encoding='utf-8') as f:
        db.quotes.insert_many(json.load(f))

    return "Данные успешно импортированы в MongoDB Atlas!"


if __name__ == "__main__":
    URL = "mongodb+srv://cats12:Mars1221@cats.5itvvh7.mongodb.net/?appName=cats"
    result = upload_data(URL)
    print(result)