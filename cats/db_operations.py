import pymongo 


#   Возвращает список всех котов из коллекции
def get_all_cats(collection):
    return list(collection.find())

#   Поиск кота по имени
def get_cat_by_name(collection, name):
    return collection.find_one({'name': name})

#   Обновить возраст кота через его имя. Вернёт True, если успешно.
def update_cat_age(collection, name, new_age):
    return collection.update_one({'name': name}, {'$set': {'age': new_age}})
    

    # Добавить характеристику в features. Вернёт True, если успешно.
def add_cat_feature(collection, name, feature):
    return collection.update_one({'name': name}, {'$push': {'features': feature}})
   

#   Удалить кота из коллекции по имени. Вернёт True, если успешно.
def delete_cat_by_name(collection, name):
    return collection.delete_one({'name': name})
    

#   Удалить все записи из коллекции.
def delete_all_cats(collection):
    return collection.delete_many({})
    