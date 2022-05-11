# ANALYSIS OF GLOBAL ENERGY DEMAND (AGED)

## Description:
Energy has remained a hot topic for centuries. It is what has powered civilizations through thick and thin. In nearly every case, energy has transformed standards of living, infrastructure, opportunities, and the quality of life in that specific area. The need for visualizing and understanding the investments countries around the world are making overtime in the energy sector is more important than ever before. Additionally, this application is important because it can be used to reveal what countries have done in terms of climate change and how it has affected not only themselves but the rest of the planet. We can visualize the growth/decay of a wide variety of trends using this API including renewable energy, fossil fuels, GDP, population, and much more! There are 119 total trends that can be viewed and analyzed using our API. The plots and visualizations generated from our API can generate deeper insights on the outcomes of investing, producing, and consuming certain types of energy. Our target audience for our API is specifically environmentalists, energy industry professionals, economists, and engineers that want to visualize the growth of certain energy sources in specific parts of the world.

## How to Load API to your Local Repository:
In order to begin interacting with this API, we need to load the API successfully into our Local Repository. Here are the steps outlined below:
1) Open up a brand new terminal on your computer (e.g. Windows Powershell, etc.)
2) Once you have successfully ssh'ed into ISP on the TACC Computer server, please create a brand new directory by running this command: `mkdir <nameofdirectory>`
3) Next, run this command to pull all of the relevant files for the API into your local machine: `git clone git@github.com:Vjannu0711/AGED.git`
4) Hit `ls` after the machine shows that it has successfully loaded the files into the machine to check that all of the files are present in your directory on your machine.
5) Next, we need to load and set up the Flask environment on our computer. Simply type the three commands into your command line terminal one-by-one in this order:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5000
```

## How to Interact with API:
```
/help                                                  (GET) Information on how to interact with the application
/read                                                  (POST) Transfer data from file
/countries                                             (GET) All Countries from the data set
/countries/<country>/year                              (GET) All information about a specific Country in a specific year
/trend/<country>/<field>                               (GET) All information on a specific field for a specific country
/create/<country>/<year>                               (POST) Create new country and year, adding it to data set
/update/<country>/<year>/<field>/<newvalue>            (PUT) Updates current country, year, and field with new data point
/delete/<country>/<year>                               (DELETE) Delete all information about a specific country and year
```

Before you run any of the routes after `/read`, you must run this command `curl localhost:5004/read -X POST` in order to read the data and load it into Redis database.
You will get this message confirming that the data has been successfully gathered and loaded into Redis: `Data gathered`

## Description of Outputs:

Input: `curl localhost:5004/countries/Italy/2005`

Output:
```
  "iso_code": "ITA",
  "country": "Italy",
  "year": "2005",
  "coal_prod_change_pct": "-3.061",
  "coal_prod_change_twh": "-0.023",
  "gas_prod_change_pct": "-6.864",
  "gas_prod_change_twh": "-8.536",
  "oil_prod_change_pct": "11.739",
  "oil_prod_change_twh": "7.466",
  "energy_cons_change_pct": "0.16",
  "energy_cons_change_twh": "3.489",
  "biofuel_share_elec": "1.579",
  "biofuel_elec_per_capita": "80.129",
  "biofuel_cons_change_pct": "-29.815",
  "biofuel_share_energy": "0.088",
  "biofuel_cons_change_twh": "-0.821",
  "biofuel_consumption": "1.933",
  "biofuel_cons_per_capita": "33.163",
  "carbon_intensity_elec": "399.0",
  "coal_share_elec": "14.747",
 ........................... (more info)
  "population": "58281212.0",
  "primary_energy_consumption": "2190.923",
  "renewables_elec_per_capita": "830.971",
  "renewables_share_elec": "16.377",
  "renewables_cons_change_pct": "-11.008",
  "renewables_share_energy": "6.035",
  "renewables_cons_change_twh": "-16.355",
  "renewables_consumption": "132.228",
  "renewables_energy_per_capita": "2268.787",
  "solar_share_elec": "0.01",
  "solar_cons_change_pct": "6.22",
  "solar_share_energy": "0.004",
  "solar_cons_change_twh": "0.005",
  "solar_consumption": "0.083",
  "solar_elec_per_capita": "0.515",
  "solar_energy_per_capita": "1.431",
  "wind_share_elec": "0.791",
  "wind_cons_change_pct": "26.051",
  "wind_share_energy": "0.288",
  "wind_cons_change_twh": "1.303",
  "wind_consumption": "6.302",
  "wind_elec_per_capita": "40.15",
  "wind_energy_per_capita": "108.137"
  ```
  
  Input: `curl localhost:5004/trend/Afghanistan/population`
  
  Output:
  ```
  [
  "1900 - 4832414.0",
  "1901 - 4879685.0",
  "1902 - 4935122.0",
  "1903 - 4998861.0",
  "1904 - 5063419.0",
  "1905 - 5128808.0",
  "1906 - 5195038.0",
  "1907 - 5262120.0",
  "1908 - 5330065.0",
  "1909 - 5467828.0",
  "1910 - 5681487.0",
  "1911 - 5977589.0",
  "1912 - 6363186.0",
  "1913 - 6845878.0",
  "1914 - 7365181.0",
  "1915 - 7923871.0",
  "1916 - 8524936.0",
  "1917 - 9171589.0",
  "1918 - 9875230.0",
  "1919 - 10338650.0",
......................
  "1995 - 18110662.0",
  "1996 - 18853444.0",
  "1997 - 19357126.0",
  "1998 - 19737770.0",
  "1999 - 20170848.0",
  "2000 - 20779958.0",
  "2001 - 21606992.0",
  "2002 - 22600774.0",
  "2003 - 23680872.0",
  "2004 - 24726690.0",
  "2005 - 25654274.0",
  "2006 - 26433058.0",
  "2007 - 27100542.0",
  "2008 - 27722282.0",
  "2009 - 28394806.0",
  "2010 - 29185512.0",
  "2011 - 30117410.0",
  "2012 - 31161378.0",
  "2013 - 32269592.0",
  "2014 - 33370804.0",
  "2015 - 34413600.0",
  "2016 - 35383028.0",
  "2017 - 36296108.0",
  "2018 - 37171920.0",
  "2019 - 38041756.0",
  "2020 - No Data"
  ```


## How to Submit a Job:
Input: `curl localhost:5004/jobs`

Output: 
```
To submit a job, do the following:
curl localhost:5004/jobs -X POST -d '{"country":<country>, "field":<field>, "start":<year>, "end":<year>}' -H "Content-Type: application/json"
```

Example Input: `curl localhost:5004/jobs -X POST -d '{"country":"Spain", "field":"gdp", "start":"2000", "end":"2008"}' -H "Content-Type: application/json"`

Output:
```
{
  "id": "68005b49-25c1-42fc-89be-e3e9867121aa",
  "datetime": "2022-05-11 15:15:36.249426",
  "country": "Spain",
  "field": "gdp",
  "status": "submitted",
  "start": "2000",
  "end": "2008"
}
```
Check the status of the job by copying and pasting the "id" number from the previous command's output:
`curl localhost:5004/jobs/68005b49-25c1-42fc-89be-e3e9867121aa`
Output:
```
{
  "id": "68005b49-25c1-42fc-89be-e3e9867121aa",
  "datetime": "2022-05-11 15:15:36.249426",
  "country": "Spain",
  "field": "gdp",
  "status": "finished",
  "start": "2000",
  "end": "2008"
}
```
As we can see above, it says that the job has "finished". Now we must obtain the image of our desired visualization plot by running the command below:
`curl localhost:5004/download/68005b49-25c1-42fc-89be-e3e9867121aa >output.png`
Note that we pasted the same job "id" as above.

Output for this command should look something like this which shows that the image has been created:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19390  100 19390    0     0  1765k      0 --:--:-- --:--:-- --:--:-- 1893k
```
