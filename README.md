$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
flask run
#psql -U postgres -h localhost -p 5432