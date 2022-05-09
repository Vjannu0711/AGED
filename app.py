from flask import Flask, jsonify
import csv
import logging
import os
import redis

redis_ip=os.environ.get('REDIS_IP')
rd = redis.Redis(host=redis_ip, port=6379, db=0)

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
    unique_countries_list = []

    for d in data:                       #Call on specific key
        countries_list.append(d['country'])

    unique_countries_list = list(set(countries_list))
    return(jsonify(unique_countries_list))

@app.route('/countries/<country>/<year>',methods=['GET'])
def country_specs(country, year):
    for d in data:
        spec_year = d['year']
        spec_country = d['country']
        if country == spec_country and year == spec_year:
            return(d)
        return(True)

@app.route('/countries/<country>/<field>',methods=['GET'])
def countries_field(country, field):
    for d in data:
        fs = str(field)
        spec_country = d['country']
        if country == spec_country:
            spec_data = []
            spec_data.append(d[fs])
    return(jsonify(spec_data))


#@app.route('/create/<country>/<year>', methods=['CREATE'])
#def create_CountryYear(country, year):

@app.route('/delete/<country>/<year>', methods=['DELETE'])
def delete_CountryYear(country, year):
    rd.delete(f'{country}-{year}')
    return(f'This {country}and {year} has been deleted')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    return(f'This {country}and {year} has been deleted')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
