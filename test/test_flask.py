import json
import os
import re
import time

import pytest
import requests

api_host = 'localhost'
api_port = '5004'
api_prefix = f'http://{api_host}:{api_port}'

def test_data_download():
    route = f'{api_prefix}/read'
    response = requests.post(route)
    assert response.ok == True
    assert response.content == b'Data gathered\n'

def test_data_get():
    route = f'{api_prefix}/countries'
    response = requests.get(route)
    assert response.ok == True

def test_jobs_info():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)
    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job, do the following', response.text)) == True

def test_jobs_cycle():
    route = f'{api_prefix}/jobs'
    job_data = {'country':'Zimbabwe', 'field':'gdp', 'start':'2005', 'end':'2015'}
    response = requests.post(route, json=job_data)

    assert response.ok == True
    assert response.status_code == 200

    UUID = response.json()['id']
    assert isinstance(UUID, str) == True
    assert response.json()['status'] == 'submitted'

    time.sleep(15)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)
