from flask import Flask, jsonify
import csv
import logging

app = Flask(__name__)

data = []
@app.route('/read', methods=['POST'])
def read():
    global data
    with open('owid-energy-data.csv', 'r') as f:
        DF = csv.DictReader(f)
        for row in DF:
            data.append(dict(row))      #Set keys per dictionary redis
        return('Data gathered')

@app.route('/countries',methods=['GET'])
def all_Countries():
    logging.info("Gathering all countries...")
    countries_list = []
    unique_countries_list = []

    for d in data:                       #Call on specific key
        countries_list.append(d['country'])

    unique_countries_list = list(set(countries_list))
    return(jsonify(unique_countries_list))

#@app.route('/create/<country>/<year>', methods=['CREATE'])
#def create_CountryYear(country, year);

@app.route('/delete/<country>/<year>', methods=['DELETE'])
def delete_CountryYear(country, year):
    rd.delete(f'{country}-{year}')
    return(f'This {country}and {year} has been deleted')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
