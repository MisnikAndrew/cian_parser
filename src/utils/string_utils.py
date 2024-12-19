import re
import json

def write_to_file(file_path: str, text: str):
    with open(file_path, "w") as text_file:
        text_file.write(text)

def get_int_from_str(str: str):
    str = str.replace('\xa0', '')
    str = re.sub("[^0-9]", "", str)
    ans = 0
    for c in str:
        if c >= '0' and c <= '9':
            ans *= 10
            ans += (int)(c) - (int)('0')
    return ans

def find_line_with_substring(multiline_str, substring):
    lines = multiline_str.splitlines()
    for line in lines:
        if substring in line:
            return line
    return None

def get_value(json, path, toString=True):
    for p in path:
        if p in json.keys():
            json = json[p]
        else:
            return 'UNDEF'
    if toString == False:
        return json
    if json == True:
        return 'Да'
    if json == False:
        return 'Нет'
    if json == 'euro':
        return 'Евро'
    if json == 'cosmetic':
        return 'Косметический'
    if json == 'design':
        return 'Дизайнерский'
    if json == 'yardAndStreet':
        return 'На улицу и двор'
    if json == 'yard':
        return 'Во двор'
    if json == 'street':
        return 'На улицу'
    return str(json)

def underground_to_value(underground):
    ans = ''
    for station in underground.keys():
        ans += station + ': ' + str(underground[station]['time']) + ' мин. '
        if underground[station]['type'] == 'walk':
            ans += 'пешком; '
        else:
            ans += 'на транспорте; '
    return ans

def parse_undergrounds(json):
    values = {}
    for station in json:
        value = {}
        value['time'] = get_value(station, ['travelTime'], False)
        value['type'] = get_value(station, ['travelType'], False)
        values[get_value(station, ['name'])] = value
    return values

def write_as_text(cnt, values):
    ans = '\n' + 'Квартира № ' + str(cnt)
    for [key, value] in values.items():
        if key == 'underground_values':
            continue
        ans += '\n' + key + ': ' + str(value)
    ans += '\n\n\n'
    return ans

def get_values_from_object(href, objectResult):
    values = {
        'Ссылка': href
    }
    values['Цена'] = get_value(objectResult, ['value', 'offerData', 'offer', 'bargainTerms', 'price'])
    values['Месяцы предоплаты'] = get_value(objectResult, ['value', 'offerData', 'offer', 'bargainTerms', 'prepayMonths'], False)
    values['Депозит'] = get_value(objectResult, ['value', 'offerData', 'offer', 'bargainTerms', 'deposit'], False)
    values['Комиссия'] = get_value(objectResult, ['value', 'offerData', 'offer', 'bargainTerms', 'agentFee'], False)

    values['Апартаменты'] = get_value(objectResult, ['value', 'offerData', 'offer', 'isApartments'])
    values['Общая площадь'] = get_value(objectResult, ['value', 'offerData', 'offer', 'totalArea'], False)
    values['Жилая площадь'] = get_value(objectResult, ['value', 'offerData', 'offer', 'livingArea'], False)
    values['Площадь кухни'] = get_value(objectResult, ['value', 'offerData', 'offer', 'kitchenArea'], False)
    values['Этаж'] = get_value(objectResult, ['value', 'offerData', 'offer', 'floorNumber'], False)
    values['Обновлено'] = get_value(objectResult, ['value', 'offerData', 'offer', 'humanizedEditDate'])
    values['Лоджии'] = get_value(objectResult, ['value', 'offerData', 'offer', 'loggiasCount'], False)
    values['Балконы'] = get_value(objectResult, ['value', 'offerData', 'offer', 'balconiesCount'], False)
    values['Окна'] = get_value(objectResult, ['value', 'offerData', 'offer', 'windowsViewType'])
    values['Разделенные с/у'] = get_value(objectResult, ['value', 'offerData', 'offer', 'separateWcsCount'], False)
    values['Совмещенные с/у'] = get_value(objectResult, ['value', 'offerData', 'offer', 'combinedWcsCount'], False)
    values['Ремонт'] = get_value(objectResult, ['value', 'offerData', 'offer', 'repairType'])
    values['Посудомойка'] = get_value(objectResult, ['value', 'offerData', 'offer', 'hasDishwasher'])
    values['Кондиционер'] = get_value(objectResult, ['value', 'offerData', 'offer', 'hasConditioner'])
    values['Можно с детьми'] = get_value(objectResult, ['value', 'offerData', 'offer', 'childrenAllowed'])
    values['Можно с животными'] = get_value(objectResult, ['value', 'offerData', 'offer', 'petsAllowed'])
    values['Количество комнат'] = get_value(objectResult, ['value', 'offerData', 'offer', 'roomsCount'], False)

    values['Год постройки'] = get_value(objectResult, ['value', 'offerData', 'offer', 'building', 'buildYear'])
    if (values['Год постройки'] == 'UNDEF'):
        values['Год постройки'] = get_value(objectResult, ['value', 'offerData', 'bti', 'houseData', 'yearRelease'])

    values['Количество этажей'] = get_value(objectResult, ['value', 'offerData', 'offer', 'building', 'floorsCount'])
    if (values['Количество этажей'] == 'UNDEF'):
        values['Количество этажей'] = get_value(objectResult, ['value', 'offerData', 'bti', 'houseData', 'floorMax'])

    values['Высота потолков'] = get_value(objectResult, ['value', 'offerData', 'offer', 'building', 'ceilingHeight'])
    values['Количество подъездов'] = get_value(objectResult, ['value', 'offerData', 'bti', 'houseData', 'entrances'])
    values['Количество лифтов в доме'] = get_value(objectResult, ['value', 'offerData', 'bti', 'houseData', 'lifts'])
    values['Количество квартир в доме'] = get_value(objectResult, ['value', 'offerData', 'bti', 'houseData', 'flatCount'])


    underground_values = parse_undergrounds(get_value(objectResult, ['value', 'offerData', 'offer', 'geo', 'undergrounds'], False))
    values['underground_values'] = underground_values
    values['Близость к метро'] = underground_to_value(underground_values)
    return values

