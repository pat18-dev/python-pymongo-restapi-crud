$env:FLASK_APP = "src/app.py"
$env:FLASK_ENV = "development"
flask run
psql -U postgres -h localhost -p 5432
apk update
apk add nano
echo "host    all             all              0.0.0.0/0                       md5" >> pg_hba.conf
echo "host    all             all              ::/0                            md5" >> pg_hba.conf


UPDATE ticket SET name='ANDRADE/PUMA/GHIAN BENITO',levelid=2,gradeid=3,categoryid='R',write_uid=0,write_at=NOW() WHERE id = 3