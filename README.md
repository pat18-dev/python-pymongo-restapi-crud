$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
flask run
#psql -U postgres -h localhost -p 5434
apk update
apk add nano
echo "host    all             all              0.0.0.0/0                       md5" >> pg_hba.conf
echo "host    all             all              ::/0                            md5" >> pg_hba.conf