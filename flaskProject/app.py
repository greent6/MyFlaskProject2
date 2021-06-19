from flask import Flask,render_template

import requests
import config_project

app = Flask(__name__)


@app.route('/')
def index():
    try:
        theaters_data = get_data()
        cleaned_theaters_data = prepare_data(theaters_data)
    except Exception as e:
        return render_template('error.html', err=str(e))

    return render_template('index.html', data=cleaned_theaters_data)

def get_data():
    theaters_url = config_project.API_MAIN_URL + '/stat_theaters_svod/$'

    params = {
        's': 0,
        'l': 10
    }

    headers = {
        'X-API-KEY': config_project.API_KEY
    }

    r = requests.get(theaters_url, params=params, headers=headers)
    if not r.ok:
        raise Exception('failed to get dataset rows count: {0}'.format(r.text))

    total = r.json()['total']

    result = []

    while len(result) < total:
        print('loading with params: ', params)
        r = requests.get(theaters_url, params=params, headers=headers)
        if not r.ok:
            raise Exception('failed to get dataset rows count: {0}'.format(r.text))
        print('loaded data with params: ', params)

        j = r.json()
        if 'data' in j and j['data'] is not None:
            for element in j['data']:
                result.append(element)
        params['s'] += 10

    print('Rows returned: ', len(result))

    return result

def prepare_data(theaters_data):
    theaters = []

    for element in theaters_data:
        if'data' in element and element['data'] is not None:
            cell = element['data']

            if 'f_290_9nk_name' in cell and 'f_290_9nk_1' in cell and cell['f_290_9nk_name'] != 'Всего по Российской Федерации':
                theaters.append({
                    'region_name': cell['f_290_9nk_name'],
                    'theaters_count': cell['f_290_9nk_1'],
                })

    print('Number of regions: ', len(theaters))

    return theaters


if __name__ == '__main__':
    app.run()
