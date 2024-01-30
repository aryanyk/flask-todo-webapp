# remember to create main file name app.py
make two folder static and templates

#helps to create a DB 
from app import app,db
>>> app.app_context().push()
>>>  db.create_all()