# IMPORT MODULES (SETUP)
from flask import Flask, jsonify, request, send_file
import csv
import logging
import os
import redis
import json
from jobs import rd, q, add_job, get_job_by_id, jdb, img_db

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
@app.route('/trend/<country>/<field>',methods=['GET'])
def countries_field(country, field):
    trend = []
    start = int(request.args.get('start', 1900))
    end = int(request.args.get('end', 2020))+1
    for year in range(start, end):
        result = rd.hget(f'{country}-{year}', field)
        if not result:
            result = 'No Data'
        trend.append(f'{year} - {result}')
    return json.dumps(trend, indent=2)

# CREATE (CRUD)
@app.route('/create/<country>/<year>', methods=['POST'])
def create_CountryYear(country, year):
    rd.hset(f'{country}-{year}', mapping={'country': country, 'year': year})
    return(f'A new entry with your desired country and year has been entered into the system.')

# UPDATE (CRUD)
@app.route('/update/<country>/<year>/<field>/<newvalue>', methods =['PUT'])
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

# ANALYSIS API
@app.route('/jobs', methods=['POST', 'GET'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['country'], job['field'], job['start'], job['end']), indent=2) + '\n'

    elif request.method == 'GET':
        redis_dict = {}
        for key in jdb.keys():
            redis_dict[str(key)] = {}
            redis_dict[str(key)]['datetime'] = jdb.hget(key, 'datetime')
            redis_dict[str(key)]['status'] = jdb.hget(key, 'status')
        return json.dumps(redis_dict, indent=4) + '\n' + """
  To submit a job, do the following:
  curl localhost:5004/jobs -X POST -d '{"country":<country>, "field":<field>, "start":<year>, "end":<year>}' -H "Content-Type: application/json"
"""
# CHECK STATUS OF SUBMITTED JOB
@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid: str):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'

# DOWNLOAD IMAGE
@app.route('/download/<job_uuid>', methods=['GET'])
def download(job_uuid):
    path = f'/app/{job_uuid}.png'
    with open(path, 'wb') as f:
        f.write(img_db.hget(f'job.{job_uuid}', 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
