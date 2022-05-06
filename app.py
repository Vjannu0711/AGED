from flask import Flask
import csv
import logging
import pandas as pd

app = Flask(__name__)

DF = {}
@app.route('/read_data', methods=['POST'])
def data_read():
    """
    This route reads the CSV data file and sends a confirmation message to the user that the file has been read.
    """
    global DF

    fields = ['country','year','coal_production','electricity_generation','biofuel_electricity','coal_electricity','fossil_electricity','gas_electricity','hydro_electricity','nuclear_electricity','oil_electricity','renewables_electricity','oil_production','population','gdp','solar_electricity','wind_electricity','energy_per_gdp','energy_per_capita','fossil_share_elec','gas_share_elec','gas_production','low_carbon_share_elec']
    DF = pd.read_csv("owid-energy-data.csv", usecols=fields)
    #Filter on year >=1985
    DF=DF[DF['year']>=1990]
    #Filter on countries 
    Countries=['Australia','Austria','Belgium','Canada','Chile','Colombia','Costa Rica','Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy', 'Japan', 'South Korea', 'Latvia', 'Lithuania', 'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom','United States'] # OECD COUNTRIES
    #filter columns
    DF=DF.loc[DF['country'].isin(Countries)]
    #data = {}
    #data['energy'] = []
    #with open('owid-energy-data.csv', 'r') as f:
    #    reader = csv.DictReader(f)
    #    for row in reader:
    #        data['energy'].append(dict(row))
    t = type(DF)
    return f'{DF}'

#@app.route('/new_csv', methods=['POST'])
#def create_csv():
#    """
#    This route creates a new CSV from the dataframe.
#    """
#    DF.to_csv(oecd, encoding='utf-8', index=False)
#    return 'file has been created'

@app.route('/countries',methods=['GET'])
def all_Countries():
    logging.info("Gathering all countries...")
    COUNTRIES = {}
    for i in range(len(DF[Countries])):
        spec_country = DF[Countries][i]['country']
        if spec_country in COUNTRIES:
            COUNTRIES[spec_country] += 1
        else:
            COUNTRIES[spec_country] = 1
    return 

@app.route('/countries/<country>/years',methods=['GET'])
def all_fields(country):
    logging.info("Gathering all fields in /"+country)
    YEARS = {}
    for i in range(len(DF[Countries])):
        spec_country = DF[Countries][i]['country']
        if country == spec_country:
            spec_year = DF[Countries][i]['years']
            if spec_year in YEARS:
                YEARS[spec_year] += 1
            else:
                YEARS[spec_year] = 1
    return YEARS

@app.route('/countries/<country>/year/<years>/fields',methods=['GET'])
def all_cities(country, years):
    logging.info("Gathering all cities in /"+regions)
    FIELDS = {}
    for i in range(len(DF[Countries])):
        spec_country = DF[Countries][i]['country']
        if country == spec_country:
            spec_year = DF[Countries][i]['years']
            if year == spec_year:
                spec_fields = Df[Countries][i]['fields']
                if spec_fields in FIELDS:
                    FIELDS[spec_fields] +=1
                else:
                    FIELDS[spec_fields]=1
    return FIELDS

@app.route('/countries/<country>/regions/<regions>/cities/<cities>',methods=['GET'])
def specific_City(country, regions, cities):
    logging.info("Gathering info on /"+cities)
    list_of_cities = []
    list_city_data = ['spacecraft', 'sighting_date','duration_minutes','max_elevation','enters',\
'exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(ISS_Sighting_Data['visible_passes']['visible_pass'])):
        spec_country = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['country']
        if country == spec_country:
            spec_region = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['region']
            if regions == spec_region:
                spec_city = ISS_Sighting_Data['visible_passes']['visible_pass'][i]['city']
                if cities == spec_city:
                    city_dict = {}
                    for j in list_city_data:
                        city_dict[j] = ISS_Sighting_Data['visible_passes']['visible_pass'][i][j]
                    list_of_cities.append(city_dict)
    return json.dumps(list_of_cities, indent=2)
