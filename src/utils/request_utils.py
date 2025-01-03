import requests
import time
import random

timing = 0.2
try_early = 0.25
retry_early = 60.0
try_late = 0.25
retry_early = 45.0
retry_prob = 0.01

def get_sleep_time(retry, request_it):
    if request_it < 10 and retry == False:
        return try_early
    if request_it < 10 and retry == True:
        return retry_early
    if request_it >= 10 and retry == False:
        return try_late
    if request_it >= 10 and retry == True:
        return retry_early

def get_wait_time(iters):
    ans = timing * iters
    for it in range(iters):
        ans += get_sleep_time(False, it + 1)
        rnd = random.random()
        while rnd < retry_prob:
            ans += get_sleep_time(True, it + 1)
            rnd = random.random()
    return ans

def poll_request(url: str, request_it):
    sleep_interval = 1.0
    response = requests.get(url)
    time.sleep(get_sleep_time(False, request_it))
    while response.status_code == 500 or 'rate_limit' in response.text:
        if response.status_code == 500:
            print('got 500 status, trying more')
        elif 'rate_limit' in response.text:
            print('rate limited, trying more')
        time.sleep(get_sleep_time(True, request_it) * sleep_interval)
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