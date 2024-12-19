import requests
import time

def poll_request(url: str, first_sleep, sleep_interval):
    response = requests.get(url)
    time.sleep(first_sleep)
    while response.status_code == 500 or 'rate_limit' in response.text:
        if response.status_code == 500:
            print('got 500 status, trying more')
        elif 'rate_limit' in response.text:
            print('rate limited, trying more')
        time.sleep(sleep_interval)
        sleep_interval *= 1.5
        response = requests.get(url)
    return response

def create_url_from_params(min_cost, max_cost, room1, room2, room3, room4, limit, page, min_area, max_area, sort):
    params = {
        'deal_type': 'rent',
        'engine_version': '2',
        'offer_type': 'flat',
        'region': '1',
        'type': '4'
    }
    if min_cost != 0:
        params['minprice'] = str(min_cost)
    if max_cost != 0:
        params['maxprice'] = str(max_cost)
    if min_area != 0:
        params['minarea'] = str(min_area)
    if max_area != 0:
        params['maxarea'] = str(max_area)
    if sort != '':
        params['sort'] = sort
    if room1 != 0:
        params['room1'] = str(room1)
    if room2 != 0:
        params['room2'] = str(room2)
    if room3 != 0:
        params['room3'] = str(room3)
    if room4 != 0:
        params['room4'] = str(room4)
    if limit != 0:
        params['limit'] = str(limit)
    if page != 0:
        params['p'] = str(page)

    url = 'https://www.cian.ru/cat.php?'
    for param_name, param_value in params.items():
        url += param_name + '=' + param_value + '&'
    while url.endswith('&'):
        url = url[:-1]
    return url