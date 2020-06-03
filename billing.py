from app import db
from app.models import Contract
import datetime

time = str(datetime.datetime.today()).split(' ')[0].split('-')[2]

all_contracts = Contract.query.all()

for contract in all_contracts:
    print(str(contract.id) + ' ' + str(contract.date) + ' ' + str(time))
    if int(contract.date) == int(time):
        edited = Contract.query.filter_by(id=contract.id).update({'paid': int(contract.paid) - 1})
        db.session.commit()
