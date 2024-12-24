from aiogram.types import InputFile
from bs4 import BeautifulSoup
import json
import pandas as pd

from utils.request_utils import poll_request, create_url_from_params
from utils.scoring_utils import get_flat_score
from utils.string_utils import find_line_with_substring, write_as_text, get_values_from_object


def build_report(min_cost, max_cost, min_room, max_room, overall_limit, min_area):
    room1 = 0
    room2 = 0
    room3 = 0
    room4 = 0
    if min_room <= 1 and max_room >= 1:
        room1 = 1
    if min_room <= 2 and max_room >= 2:
        room2 = 1
    if min_room <= 3 and max_room >= 3:
        room3 = 1
    if min_room <= 4 and max_room >= 4:
        room4 = 1

    max_area = 0
    sort = 'creation_date_desc'
    limit = 100
    page_number = 100

    lists = {
        'Ссылка': [],
        'Цена': [],
        'Flat Score': [],
        'Underground Score': [],
        'Underground Place': [],
        'Близость к метро': [],
        'Количество комнат': [],
        'Общая площадь' : [],
        'Жилая площадь': [],
        'Площадь кухни': [],
        'Этаж': [],
        'Количество этажей': [],
        'Депозит': [],
        'Месяцы предоплаты': [],
        'Ремонт': [],
        'Апартаменты': [],
        'Лоджии': [],
        'Балконы': [],
        'Окна': [],
        'Разделенные с/у': [],
        'Совмещенные с/у': [],
        'Посудомойка': [],
        'Кондиционер': [],
        'Можно с детьми': [],
        'Можно с животными': [],
        'Обновлено': [],
        'Высота потолков': [],
        'Количество подъездов': [],
        'Количество лифтов в доме': [],
        'Количество квартир в доме': [],
    }

    cnt = 0
    result = ''
    disp_result = ''
    found = {}

    request_it = 0

    stop = False

    for page in range(page_number):
        if stop == True:
            break
        url = create_url_from_params(min_cost, max_cost, room1, room2, room3, room4, limit, page + 1, min_area, max_area, sort)
        request_it += 1
        response = poll_request(url, request_it)
        soup = BeautifulSoup(response.text, 'html.parser')
        apartments = soup.find_all('div', {'data-name': 'LinkArea'})

        for i in range (len(apartments)):
            if i % 2:
                continue
            href = apartments[i].find('a', {'class': '_93444fe79c--link--eoxce'})["href"]
            if href not in found.keys():
                found[href] = 'true'
                request_it += 1
                response = poll_request(href, request_it)

                substring = "window._cianConfig['frontend-offer-card']"
                prefix_str = "window._cianConfig['frontend-offer-card'] = (window._cianConfig['frontend-offer-card'] || []).concat("
                info = find_line_with_substring(response.text, substring)
                if info is not None:
                    info = info[:-2]
                if info is not None:
                    info = info[len(prefix_str):]

                jsonInfo = json.loads(info)
                objectResult = None
                for object in jsonInfo:
                    if object['key'] == 'defaultState':
                        objectResult = object
                if (objectResult is None):
                    print('object is None')
                    continue

                values = get_values_from_object(href, objectResult)
                score = get_flat_score(values, max_cost)
                values['Flat Score'] = str(round(score[0]))
                values['Underground Score'] = str(round(score[1], 2))
                values['Underground Place'] = str(score[2])

                cnt += 1
                if cnt % 5 == 0:
                    print('done: ' + str(cnt) + ' / ' + str(min(len(apartments) // 2 * page_number, overall_limit)))

                result += write_as_text(cnt, values)
                if (cnt <= 3):
                    disp_result += write_as_text(cnt, values)
                for key in lists.keys():
                    lists[key].append(values.get(key, ''))

                if cnt >= overall_limit:
                    stop = True
                    break
    dataframe = pd.DataFrame(lists)
    csv_file_path = 'report_table.csv'
    dataframe.to_csv(csv_file_path)
    csv_file = InputFile(csv_file_path)

    txt_file_path = 'report.txt'
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(result)
    txt_file = InputFile(txt_file_path)

    return disp_result, csv_file, txt_file