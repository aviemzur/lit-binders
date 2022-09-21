import json

import requests

BASE_URL = "https://api.scryfall.com"
SITE_CARD_URL = "https://scryfall.com/card/"


def _url(url):
    return BASE_URL + url


def get_cards(ids):
    if type(ids) == str:
        return get_url(_url('/cards/' + ids))

    results = []

    for id in ids:
        results.append(get_url(_url('/cards/' + id)))

    return results


def get_url(url):
    res = requests.get(url)
    return json.loads(res.content)


def get_data_url(output, url):
    res = requests.get(url)
    res = json.loads(res.content)
    output += res.get('data', [])
    if res.get('has_more', False):
        get_data_url(output, res['next_page'])


def url_to_id(url):
    if url.startswith(SITE_CARD_URL):
        id = url.replace(SITE_CARD_URL, '')
        separator_indexes = list(_findall('/', id))
        result = id[:separator_indexes[1]]
        if '|' in url:
            _, suffix = url.split('|')
            return f'{result}|{suffix}'
        return result
    return 'blank'


def _findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)


pass
