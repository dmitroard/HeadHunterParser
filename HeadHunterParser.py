# -*- coding: cp1251 -*-
import requests
import pandas as pd

#Список строк для парса
basic_titles = ["продуктовый аналитик", "системный аналитик", "риск-аналитик"]

def parse_vacancies(titles: list, max_page: int = 100, locate: int = 1, file_names: list = []) -> int:
    """
    Функция парсировки сайта HH.ru

    Параметры
    ---------------------------------------------------------------------------------
    titles : список строк, вхождение которых ищем в вакансиях

    max_page :  максимальное кол-во строк, которые будем парсить 
                                         (всего записей максимум max_page * 20)

    file_names : список имен файлов, которые будут созданы

    locate : номер региона в api.hh
    ---------------------------------------------------------------------------------
    Итог выполнения: сохраняется n файлов, где n - длинна списка titles.
    ---------------------------------------------------------------------------------
    Подробнее -> https://github.com/hhru/api/blob/master/docs/vacancies.md#vacancy-fields
    """
    #генерируем список названий + .csv
    if(len(file_names) == 0):
        file_names = [name + ".csv" for name in titles]
    else:
        file_names = [name + ".csv" for name in file_names]
    
    for index_title in range(len(titles)):
        print("Идет поиск по запросу", titles[index_title])
        data = []
        for page in range(max_page):
            basic_link = "https://api.hh.ru/vacancies"
            parse_arguments = {"text" : titles[index_title], 
                               "area" : locate,
                               "page" : page}
            #ищем вакансию по параметрам
            request_data = requests.get(basic_link, params=parse_arguments)
            js_data = request_data.json()
            #сохраняем для дальнейшего создания датафрейма
            data.append(js_data)
        index_data = 0
        #обработка ошибки ввода капчи, потребуется вручную по ссылки пройти капчу, затем перезапустить программу
        if("errors" in data[0].keys()):
            print(data[0]["errors"][0]["captcha_url"] + "&backurl=https://ya.ru/")
            return 400
        else:
            data_columns = data[0]["items"][0].keys()
            df = pd.DataFrame(columns = data_columns)
            for index_record in range(len(data)):
                for index_item in range(len(data[index_record]["items"])):
                    data[index_record]["items"][index_item]
                    #сохраняем данные в датафрейм
                    df.loc[index_data] = data[index_record]["items"][index_item]
                    index_data += 1
            #сохраняем в файл
            df.to_csv(file_names[index_title])
            print(f"Готово, найдено {len(df)} записей")
    return 0

parse_vacancies(basic_titles, 1, 1, ["prod", "sys", "risk"])