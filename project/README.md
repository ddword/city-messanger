### The final project is web application named as City Messenger.

Based on Python - Flask + Jinja  and Javascript - Api Open Layers, mapConrol.js, html templates and Bootstrap 4, css.
  
City Messenger should help citizens to report about any problem which occurs on the streets of city and fix it.

To see all existing issues - presented as markers on the map - user should registered in app.

To report about any issue user also should be registered.

In the process of creation, I found out that there is already a slightly similar application https://montreal.ca/en/report-problem.

The one significant difference in City Messenger all addresses with problems shown on the map.

I used API of OpenLayers and API of nominatim to implement map https://nominatim.openstreetmap.org/

### To run this app on your local machine, follow these steps:
- Clone the repo project from `git clone https://github.com/ddword/city-messanger.git`
- Go into the folder: `cd city-messanger`
- If you don't have python on your machine install it.
- Install npm dependencies from package-lock.json `npm install`
- Create virtual environment for the project
- Run virtual environment, the command depends from your venv package, for example `venv activate`
- Run application in development environment.

Go into the folder: `cd city-messanger`

The commands: 

`$ export FLASK_APP=application`
`$ export FLASK_ENV=development`
`$ flask run`

Open `http://localhost:5000/` in your local browser
