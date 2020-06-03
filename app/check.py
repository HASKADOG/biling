import datetime
from app.models import Contract
from app import db

time = datetime.datetime.today()
time = str(time).split(' ')
time = str(time[0]).split('-')
print(time)