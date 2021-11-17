import requests


def get_data(url):
    """
    Делаем запрос на сайт и читаем оттуда данные в виде json
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise Exception("Проблемы с подключением к API: %s" % err)
    return r.text
