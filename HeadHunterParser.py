# -*- coding: cp1251 -*-
import requests
import pandas as pd

#������ ����� ��� �����
basic_titles = ["����������� ��������", "��������� ��������", "����-��������"]

def parse_vacancies(titles: list, max_page: int = 100, locate: int = 1, file_names: list = []) -> int:
    """
    ������� ���������� ����� HH.ru

    ���������
    ---------------------------------------------------------------------------------
    titles : ������ �����, ��������� ������� ���� � ���������

    max_page :  ������������ ���-�� �����, ������� ����� ������� 
                                         (����� ������� �������� max_page * 20)

    file_names : ������ ���� ������, ������� ����� �������

    locate : ����� ������� � api.hh
    ---------------------------------------------------------------------------------
    ���� ����������: ����������� n ������, ��� n - ������ ������ titles.
    ---------------------------------------------------------------------------------
    ��������� -> https://github.com/hhru/api/blob/master/docs/vacancies.md#vacancy-fields
    """
    #���������� ������ �������� + .csv
    if(len(file_names) == 0):
        file_names = [name + ".csv" for name in titles]
    else:
        file_names = [name + ".csv" for name in file_names]
    
    for index_title in range(len(titles)):
        print("���� ����� �� �������", titles[index_title])
        data = []
        for page in range(max_page):
            basic_link = "https://api.hh.ru/vacancies"
            parse_arguments = {"text" : titles[index_title], 
                               "area" : locate,
                               "page" : page}
            #���� �������� �� ����������
            request_data = requests.get(basic_link, params=parse_arguments)
            js_data = request_data.json()
            #��������� ��� ����������� �������� ����������
            data.append(js_data)
        index_data = 0
        #��������� ������ ����� �����, ����������� ������� �� ������ ������ �����, ����� ������������� ���������
        if("errors" in data[0].keys()):
            print(data[0]["errors"][0]["captcha_url"] + "&backurl=https://ya.ru/")
            return 400
        else:
            data_columns = data[0]["items"][0].keys()
            df = pd.DataFrame(columns = data_columns)
            for index_record in range(len(data)):
                for index_item in range(len(data[index_record]["items"])):
                    data[index_record]["items"][index_item]
                    #��������� ������ � ���������
                    df.loc[index_data] = data[index_record]["items"][index_item]
                    index_data += 1
            #��������� � ����
            df.to_csv(file_names[index_title])
            print(f"������, ������� {len(df)} �������")
    return 0

parse_vacancies(basic_titles, 1, 1, ["prod", "sys", "risk"])