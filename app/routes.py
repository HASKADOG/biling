from app import app, db
from flask import render_template, redirect, url_for, request
from app.forms import Contract_add, Set_paid, Archive, Test_one, Test_two, History_cancel, History_clear, Search, \
    Search_close, Delete_contract
from app.models import Contract, Deals
from tools import get_contracts, get_contracts_by_id, get_all_deals, get_non_deleted_deals
import datetime


# TODO
# 1) Change the way to store day data
# 2) Write the billing bot


@app.route('/')
@app.route('/index')
def index():
    return "404 NOT FOUND"


@app.route('/unpaid', methods=['GET', 'POST'])
def list():
    set = Set_paid()
    archive = Archive()
    history_cancel = History_cancel()
    history_clear = History_clear()
    search = Search()
    search_close = Search_close()
    deals = get_non_deleted_deals()
    searched = [{
        'id': 0,
        'number': 0,
        'is_arch': 0,
        'date': 0,
        'paid': 0
    }]
    status_active = ''
    bcg_stat = ''

    nav = ['Лист неоплативших',
           [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Все договоры', '/all'], ['История', '/history'],
            ['Удалить контракт', '/delete']]]
    contracts = get_contracts(Contract, 'unpaid')
    print(contracts)

    if set.validate_on_submit() and set.submit.data:
        old = Contract.query.get(set.id.data)
        name_add = str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data)
        add_deal = Deals(num=old.id, name=name_add, type='0', old_paid=old.paid, old_date=old.date, revert=False,
                         deleted=False)
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})
        db.session.add(add_deal)
        print('Deal type 0 has been added')
        db.session.commit()

        return redirect(url_for('list'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            name_add = str(old.number) + ' арихивирован'
            add_deal = Deals(num=old.id, name=name_add, type='1', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('list'))

        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            name_add = str(old.number) + ' задействован'
            add_deal = Deals(num=old.id, name=name_add, type='2', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('list'))

    if history_clear.validate_on_submit() and history_clear.clear.data:
        for deal in deals:
            change = Deals.query.filter_by(id=int(deal['id'])).update({'deleted': True})
            db.session.commit()
        return redirect(url_for('list'))

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        deal = Deals.query.filter_by(id=int(history_cancel.id.data)).first()
        contract_id = int(deal.num)
        contract = Contract.query.get(contract_id)

        if deal.type == 0:
            backed_up = Contract.query.filter_by(id=contract_id).update({'date': deal.old_date, 'paid': deal.old_paid})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 1:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'Действющий'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 2:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'В архиве'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        db.session.commit()
        return redirect(url_for('list'))

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search=search,
                           searched=searched, status_active=status_active, search_close=search_close, bcg_stat=bcg_stat)


@app.route('/add-user', methods=['GET', 'POST'])
def add():
    form = Contract_add()
    time = str(datetime.datetime.today()).split(' ')[0].split('-')
    nav = ['Добавить договор',
           [['Лист неоплативших', '/unpaid'], ['Архив', '/archive'], ['Все договоры', '/all'], ['История', '/history'],
            ['Удалить контракт', '/delete']]]
    history_cancel = History_cancel()
    history_clear = History_clear()
    deals = get_non_deleted_deals()

    if form.validate_on_submit():
        contract = Contract(number=form.number.data, is_arch=form.is_arch.data, date=form.date.data,
                            paid=form.paid.data)
        db.session.add(contract)
        db.session.commit()
        # return redirect(url_for('quiz_2'))
        print(form.data)
    return render_template('add-user.html', form=form, time=time[2], nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel)


@app.route('/archive', methods=['GET', 'POST'])
def archive():
    set = Set_paid()
    archive = Archive()
    history_cancel = History_cancel()
    history_clear = History_clear()
    search = Search()
    search_close = Search_close()
    deals = get_non_deleted_deals()
    searched = [{
        'id': 0,
        'number': 0,
        'is_arch': 0,
        'date': 0,
        'paid': 0
    }]
    status_active = ''
    bcg_stat = ''

    nav = ['Архив', [['Лист неоплативших', '/unpaid'], ['Добавить договор', '/add-user'], ['Все договоры', '/all'],
                     ['История', '/history'], ['Удалить контракт', '/delete']]]

    contracts = get_contracts(Contract, 'archive')
    print(contracts)

    if set.validate_on_submit() and set.submit.data:
        old = Contract.query.get(set.id.data)
        name_add = str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data)
        add_deal = Deals(num=old.id, name=name_add, type='0', old_paid=old.paid, old_date=old.date, revert=False,
                         deleted=False)
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})
        db.session.add(add_deal)
        print('Deal type 0 has been added')
        db.session.commit()

        return redirect(url_for('archive'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            name_add = str(old.number) + ' арихивирован'
            add_deal = Deals(num=old.id, name=name_add, type='1', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('archive'))

        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            name_add = str(old.number) + ' задействован'
            add_deal = Deals(num=old.id, name=name_add, type='2', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('archive'))

    if history_clear.validate_on_submit() and history_clear.clear.data:
        for deal in deals:
            change = Deals.query.filter_by(id=int(deal['id'])).update({'deleted': True})
            db.session.commit()
        return redirect(url_for('archive'))

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        deal = Deals.query.filter_by(id=int(history_cancel.id.data)).first()
        contract_id = int(deal.num)
        contract = Contract.query.get(contract_id)

        if deal.type == 0:
            backed_up = Contract.query.filter_by(id=contract_id).update({'date': deal.old_date, 'paid': deal.old_paid})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 1:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'Действющий'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 2:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'В архиве'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        db.session.commit()
        return redirect(url_for('archive'))

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search=search,
                           searched=searched, status_active=status_active, search_close=search_close, bcg_stat=bcg_stat)


@app.route('/all', methods=['GET', 'POST'])
def all():
    set = Set_paid()
    archive = Archive()
    history_cancel = History_cancel()
    history_clear = History_clear()
    search = Search()
    search_close = Search_close()
    deals = get_non_deleted_deals()

    nav = ['Все договоры', [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Лист неоплативших', '/unpaid'],
                            ['История', '/history'], ['Удалить контракт', '/delete']]]
    searched = [{
        'id': 0,
        'number': 0,
        'is_arch': 0,
        'date': 0,
        'paid': 0
    }]

    status_active = ''
    bcg_stat = ''
    contracts = get_contracts(Contract, 'all')
    print(contracts)

    if set.validate_on_submit() and set.submit.data:
        old = Contract.query.get(set.id.data)
        name_add = str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data)
        add_deal = Deals(num=old.id, name=name_add, type='0', old_paid=old.paid, old_date=old.date, revert=False,
                         deleted=False)
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})
        db.session.add(add_deal)
        print('Deal type 0 has been added')
        db.session.commit()

        return redirect(url_for('all'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            name_add = str(old.number) + ' арихивирован'
            add_deal = Deals(num=old.id, name=name_add, type='1', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('all'))

        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            name_add = str(old.number) + ' задействован'
            add_deal = Deals(num=old.id, name=name_add, type='2', old_paid=old.paid, old_date=old.date, revert=False,
                             deleted=False)
            db.session.add(add_deal)
            db.session.commit()
            return redirect(url_for('all'))

    if history_clear.validate_on_submit() and history_clear.clear.data:
        for deal in deals:
            change = Deals.query.filter_by(id=int(deal['id'])).update({'deleted': True})
            db.session.commit()
        return redirect(url_for('all'))

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        deal = Deals.query.filter_by(id=int(history_cancel.id.data)).first()
        contract_id = int(deal.num)
        contract = Contract.query.get(contract_id)

        if deal.type == 0:
            backed_up = Contract.query.filter_by(id=contract_id).update({'date': deal.old_date, 'paid': deal.old_paid})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 1:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'Действющий'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        if deal.type == 2:
            backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'В архиве'})
            deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

        db.session.commit()
        return redirect(url_for('all'))

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search=search,
                           searched=searched, status_active=status_active, search_close=search_close, bcg_stat=bcg_stat)


@app.route('/history', methods=['GET', 'POST'])
def history():
    history_cancel = History_cancel()
    history_clear = History_clear()
    deals = get_all_deals()
    nav = ['История', [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Лист неоплативших', '/unpaid'],
                       ['Все договоры', '/all'], ['Удалить контракт', '/delete']]]
    if history_clear.validate_on_submit():
        if history_cancel.validate_on_submit and history_cancel.cancel.data:
            i = 0
            deal = Deals.query.filter_by(id=int(history_cancel.id.data)).first()
            contract_id = int(deal.num)
            contract = Contract.query.get(contract_id)

            if deal.type == 0:
                backed_up = Contract.query.filter_by(id=contract_id).update(
                    {'date': deal.old_date, 'paid': deal.old_paid})
                deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

            if deal.type == 1:
                backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'Действющий'})
                deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

            if deal.type == 2:
                backed_up = Contract.query.filter_by(id=contract_id).update({'is_arch': 'В архиве'})
                deleted_deal = Deals.query.filter_by(id=int(deal.id)).update({'deleted': True, 'revert': True})

            db.session.commit()
            return redirect(url_for('history'))

    return render_template('history.html', deals=deals, nav=nav, history_clear=history_clear,
                           history_cancel=history_cancel)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    history_cancel = History_cancel()
    history_clear = History_clear()
    delete_contract = Delete_contract()
    deals = get_non_deleted_deals()

    nav = [' Удалить контракт',
           [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Лист неоплативших', '/unpaid'],
            ['Все договоры', '/all'], ['История', '/history']]]

    if delete_contract.validate_on_submit():
        delete = Contract.query.filter_by(id=int(delete_contract.idd.data)).delete()
        db.session.commit()
        print('deleted')

    return render_template('delete.html', deals=deals, nav=nav, history_clear=history_clear,
                           history_cancel=history_cancel, delete_contract=delete_contract)
