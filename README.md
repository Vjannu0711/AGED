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
