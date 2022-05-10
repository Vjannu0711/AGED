from flask import Flask, jsonify
import csv
import logging
import os
import redis
import json

redis_ip=os.environ.get('REDIS_IP')
rd = redis.Redis(host=redis_ip, port=6789, db=0, decode_responses=True)

app = Flask(__name__)

#data = []
@app.route('/read', methods=['POST'])
def read():
    #global data
    with open('owid-energy-data.csv', 'r') as f:
        DF = csv.DictReader(f)
        for row in DF:
           # data.append(dict(row))      #Set keys per dictionary redis
            key = f"{dict(row)['country']}-{dict(row)['year']}"
            rd.hset(key, mapping=dict(row))
    return 'Data gathered'

@app.route('/countries',methods=['GET'])
def all_Countries():
    logging.info("Gathering all countries...")
    countries_list = []
    for d in rd.keys():                      
        countries_list.append(rd.hget(d, 'country').decode('utf-8'))
    return json.dumps(countries_list, indent=2)

@app.route('/countries/<country>/<year>',methods=['GET'])
def country_specs(country, year):
    key = f'{country}-{year}'
    return json.dumps(rd.hgetall(key), indent=2)

@app.route('/countries/<country>/<field>',methods=['GET'])
def countries_field(country, field):
    #spec_data = []
    #for d in data:
    #    fs = str(field)
    #    spec_country = d['country']
    #    if country == spec_country:
    #        spec_data.append(d[fs])
    #return(jsonify(spec_data))
    key = f'{country}'
    return json.dump(rd.hgetall(key),indent=3)


#@app.route('/create/<country>/<year>', methods=['CREATE'])
#def create_CountryYear(country, year):

@app.route('/delete/<country>/<year>', methods=['DELETE'])
def delete_CountryYear(country, year):
    rd.delete(f'{country}-{year}')
    return(f'This {country}and {year} has been deleted')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
