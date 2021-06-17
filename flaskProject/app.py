from flask import Flask,render_template

import requests
import config_project

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

def get_data():
    theaters_url = config_project.API_MAIN_URL + '/stat_theaters_svod/$'

    r = requests.get(theaters_url,params={'$':0,'l':100}, headers={'X-API-KEY': config_project.API_KEY})
    if not r.ok:
        raise Exception('failed to get dataset rows count: {0}'.format(r.text))
    print('Rows returned: ', r.json()["count"])

get_data()

if __name__ == '__main__':
    app.run()
