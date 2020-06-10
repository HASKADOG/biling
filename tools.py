from app import db
from app.models import Contract, Deals
from flask import render_template, redirect, url_for, request


def get_contracts(contract, type):
    contracts_all = []
    contracts = contract.query.all()
    if type == 'unpaid':
        for u in contracts:
            if int(u.paid) == 0 and u.is_arch == 'Действующий':
                contracts_all.append({
                    'id': u.id,
                    'number': u.number,
                    'is_arch': u.is_arch,
                    'date': str(u.date).split(' '),
                    'paid': u.paid
                })

    if type == 'archive':
        for u in contracts:
            if u.is_arch == 'В архиве':
                contracts_all.append({
                    'id': u.id,
                    'number': u.number,
                    'is_arch': u.is_arch,
                    'date': str(u.date).split(' '),
                    'paid': u.paid
                })

    if type == 'all':
        for u in contracts:
            contracts_all.append({
                'id': u.id,
                'number': u.number,
                'is_arch': u.is_arch,
                'date': str(u.date).split(' '),
                'paid': u.paid
            })

    return contracts_all


def get_contracts_by_id(id):
    out = []
    required = Contract.query.filter_by(number=id).first()
    out.append({
        'id': required.id,
        'number': required.number,
        'is_arch': required.is_arch,
        'date': str(required.date).split(' ')[0],
        'paid': required.paid
    })
    print(out)
    return out[0]


def get_all_deals():
    out = []
    required = Deals.query.all()
    for i in required:
        if i.revert:
            revert_status = 'reverted'
        else:
            revert_status = 'unreverted'

        if i.deleted:
            deleted_status = 'deleted'
        else:
            deleted_status = 'undeleted'

        out.append({
            'id': i.id,
            'name': i.name,
            'type': i.type,
            'revert': revert_status,
            'deleted': deleted_status
        })
    return (out)


def get_non_deleted_deals():
    out = []
    required = Deals.query.all()
    for i in required:
        if i.deleted == False:
            out.append({
                'id': i.id,
                'name': i.name,
                'type': i.type,
                'revert': i.revert
            })
    return (out)
