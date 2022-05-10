# IMPORT MODULES (SETUP)
from flask import Flask, jsonify
import csv
import logging
import os
import redis
import json

# SET UP REDIS
redis_ip=os.environ.get('REDIS_IP')
rd = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)

# SET UP FLASK
app = Flask(__name__)

# READ THE DATA AND LOAD TO REDIS
@app.route('/read', methods=['POST'])
def read():
    with open('owid-energy-data.csv', 'r') as f:
        DF = csv.DictReader(f)
        for row in DF:
            key = f"{dict(row)['country']}-{dict(row)['year']}"
            rd.hset(key, mapping=dict(row))
    return 'Data gathered\n'

# GET A LIST OF ALL COUNTRIES
@app.route('/countries',methods=['GET'])
def all_Countries():
    logging.info("Gathering all countries...")
    countries_list = []
    for d in rd.keys():                      
        countries_list.append(rd.hget(d, 'country'))
    return json.dumps(list(set(countries_list)), indent=2)

# GET ALL INFO FOR SPECIFIC COUNTRY AND YEAR
@app.route('/countries/<country>/<year>',methods=['GET'])
def country_specs(country, year):
    key = f'{country}-{year}'
    return json.dumps(rd.hgetall(key), indent=2)
    
# SHOW THE TREND OF A CERTAIN FIELD OVERTIME FOR SPECIFIC COUNTRY
@app.route('/countries/<country>/<field>',methods=['GET'])
def countries_field(country:str, field:str):
    trend = []
    for year in range(2009, 2010):
        result = rd.hget(f'{country}-{year}', field)
        if not result:
            result = 'No Data'
        trend.append(f'{year} - {result}')
        #trend.append(str(year) + ' ' + rd.hget(f'{country}-{year}', field))
    return json.dumps(trend, indent=2)

# CREATE (CRUD)
@app.route('/create/<country>/<year>', methods=['CREATE'])
def create_CountryYear(country, year):
    rd.hset(f'{country}-{year}', mapping={'country': country, 'year': year})
    return(f'A new entry with your desired country and year has been entered into the system.')

# UPDATE (CRUD)
@app.route('/update/<country>/<year>/<field>/<newvalue>', methods =['UPDATE'])
def update_info(country:str, year:str, field:str, newvalue:float):
    rd.hset(f'{country}-{year}', f'{field}', f'{newvalue}')
    return(f'The new value has been added to the specified field.')

# DELETE (CRUD)
@app.route('/delete/<country>/<year>', methods=['DELETE'])
def delete_CountryYear(country, year):
    key = f'{country}-{year}'
    rd.hgetall(key)
    rd.delete(key)
    return(f'All info for {country} and the year {year} has been deleted.\n')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
