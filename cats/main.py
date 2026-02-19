import pymongo
from db_operations import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Ошибка: Ведите число в поле возраса."
        except IndexError:
            return "Ошибка недостаточно аргументов!"
        except Exception as e:
            return f"Произошла ошибка: {e}"
    return inner

@input_error 
def handle_read_all(collection):
    cats = get_all_cats(collection)
    if not cats:
        return "База данных пуста."
    res = "\n Список всех котов\n" + "-"*40 + "\n"
    for cat in cats:
        res += f"Имя: {cat['name']} | Возраст: {cat['age']} | Характеристики: {', '.join(cat['features'])}\n"
    return res

@input_error
def handle_read_one(collection):
    name = input("Введите имя кота для поика: ").strip()
    cat = get_cat_by_name(collection, name)
    if cat:
        return f"Найден: {cat['name']}, возраст: {cat["age"]}, характеристика: {cat['features']} "
    return "Кот с таким именем не найден."

@input_error
def handle_update_age(collection):
    name = input("Имя кота для смены возраста: ").strip()
    new_age = int(input("Новый возраст: "))
    result = update_cat_age(collection, name, new_age)
    return "Возраст обновлен!" if result.matched_count else "Кот не найден."

@input_error 
def handle_add_feature(collection):
    name = input("Имя кота: ").strip()
    feature = input("Новая характеристика: ").strip()
    result = add_cat_feature(collection, name, feature)
    return "Характеристика добавлена!" if result.matched_count else "Кот не найден."

@input_error
def handle_delete_one(collection):
    name = input ("Имя кота для удаления: ").strip()
    result = delete_cat_by_name(collection, name)
    return f"Кот {name} удален." if result.deleted_count else "Кот не найден."

@input_error
def handle_delete_all(collection):
    confirm = input(" Вы уверены, что хотите очистить ВСЮ базу? (y/n): ")
    if confirm.lower() == 'y':
        result = delete_all_cats(collection)
        return f"База очищена. Удалено записей: {result.deleted_count}"
    return "Отмена операции."
 


def main():
    

    URL = "mongodb+srv://cats12:Mars1221@cats.5itvvh7.mongodb.net/?appName=cats"
    client = pymongo.MongoClient(URL)
    db = client["cats_db"]
    collection = db["cats"]
        

    commands = {
        "1": handle_read_all,
        "2": handle_read_one,
        "3": handle_update_age,
        "4": handle_add_feature,
        "5": handle_delete_one,
        "6": handle_delete_all
    }

    while True:
        print(f"\n{'='*10} CAT ASSISTANT CRUD {'='*10}")
        print("1. Показать всех       4. Добавить черту")
        print("2. Найти по имени      5. Удалить кота")
        print("3. Обновить возраст    6. Очистить всё")
        print("0. Выход")
        
        choice = input("\nВведите номер команды: ")

        if choice == '0':
            print("До свидания!")
            break
        
        handler = commands.get(choice)
        if handler:
            print(handler(collection))
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()