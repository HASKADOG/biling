from app import app, db
from flask import render_template, redirect, url_for, request
from app.forms import Contract_add, Set_paid, Archive, Test_one, Test_two, History_cancel, History_clear, Search, Search_close
from app.models import Contract
from tools import get_contracts, get_contracts_by_id
import datetime

# TODO
# 1) Change the way to store day data
# 2) Write the billing bot

deals = []


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/unpaid', methods=['GET', 'POST'])
def list():
    set = Set_paid()
    archive = Archive()
    history_cancel = History_cancel()
    history_clear = History_clear()
    search = Search()
    search_close = Search_close()

    searched = [{
        'id': 0,
        'number': 0,
        'is_arch': 0,
        'date': 0,
        'paid': 0
    }]
    status_active = ''
    bcg_stat = ''

    nav = ['Лист неоплативших', [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Все договоры', '/all']]]
    contracts = get_contracts(Contract, 'unpaid')
    print(contracts)

    if set.validate_on_submit() and set.submit.data:
        old = Contract.query.get(set.id.data)
        deals.append({'id': set.id.data,
                      'name': str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data),
                      'old_paid': old.paid, 'old_date': old.date, 'archived': '0'})
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})

        print(deals)
        db.session.commit()

        return redirect(url_for('list'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' архивирован',
                          'archived': 1})
            db.session.commit()
            return redirect(url_for('list'))
        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' задействован',
                          'archived': 2})
            db.session.commit()
            return redirect(url_for('list'))

    # history_form(history_clear, history_cancel, deals, Contract,'all')

    if history_clear.validate_on_submit() and history_clear.clear.data:
        print('Deals have been cleared')
        deals.clear()

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        for deal in deals:
            if deal['id'] == history_cancel.id.data:
                if deal['archived'] == 1:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'Действующий'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('all'))
                elif deal['archived'] == 2:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'В архиве'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('all'))
                else:
                    to_changes = Contract.query.filter_by(id=deal['id']).update(
                        {'paid': deal['old_paid'], 'date': deal['old_date']})
                    print(deal['old_paid'])
                    print(deal['old_date'])
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('list'))
            i += 1

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search = search, searched = searched, status_active = status_active, search_close = search_close, bcg_stat=bcg_stat)


@app.route('/add-user', methods=['GET', 'POST'])
def add():
    form = Contract_add()
    time = str(datetime.datetime.today()).split(' ')[0].split('-')
    nav = ['Добавить договор', [['Лист неоплативших', '/unpaid'], ['Архив', '/archive'], ['Все договоры', '/all']]]
    history_cancel = History_cancel()
    history_clear = History_clear()

    if form.validate_on_submit():
        contract = Contract(number=form.number.data, is_arch=form.is_arch.data, date=form.date.data, paid=form.paid.data)
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

    searched = [{
        'id': 0,
        'number': 0,
        'is_arch': 0,
        'date': 0,
        'paid': 0
    }]
    status_active = ''
    bcg_stat = ''

    nav = ['Архив', [['Лист неоплативших', '/unpaid'], ['Добавить договор', '/add-user'], ['Все договоры', '/all']]]

    contracts = get_contracts(Contract, 'archive')
    print(contracts)

    if set.validate_on_submit() and set.submit.data:
        old = Contract.query.get(set.id.data)
        deals.append({'id': set.id.data,
                      'name': str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data),
                      'old_paid': old.paid, 'old_date': old.date, 'archived': '0'})
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})

        print(deals)
        db.session.commit()

        return redirect(url_for('archive'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' архивирован',
                          'archived': 1})
            db.session.commit()
            return redirect(url_for('archive'))
        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' задействован',
                          'archived': 2})
            db.session.commit()
            return redirect(url_for('archive'))

    # history_form(history_clear, history_cancel, deals, Contract,'all')

    if history_clear.validate_on_submit() and history_clear.clear.data:
        print('Deals have been cleared')
        deals.clear()

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        for deal in deals:
            if deal['id'] == history_cancel.id.data:
                if deal['archived'] == 1:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'Действующий'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('archive'))
                elif deal['archived'] == 2:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'В архиве'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('archive'))
                else:
                    to_changes = Contract.query.filter_by(id=deal['id']).update(
                        {'paid': deal['old_paid'], 'date': deal['old_date']})
                    print(deal['old_paid'])
                    print(deal['old_date'])
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('archive'))
            i += 1

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search = search, searched = searched, status_active = status_active, search_close = search_close, bcg_stat=bcg_stat)


@app.route('/all', methods=['GET', 'POST'])
def all():
    set = Set_paid()
    archive = Archive()
    history_cancel = History_cancel()
    history_clear = History_clear()
    search = Search()
    search_close = Search_close()

    nav = ['Все договоры', [['Архив', '/archive'], ['Добавить договор', '/add-user'], ['Лист неоплативших', '/unpaid']]]
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
        deals.append({'id': set.id.data,
                      'name': str(old.number) + ' продлить на ' + str(set.paid.data) + ' с датой ' + str(set.date.data),
                      'old_paid': old.paid, 'old_date': old.date, 'archived': '0'})
        to_change = Contract.query.filter_by(id=set.id.data).update({'paid': set.paid.data, 'date': set.date.data})

        print(deals)
        db.session.commit()

        return redirect(url_for('all'))

    if archive.validate_on_submit() and archive.add.data:
        old = Contract.query.get(set.id.data)
        if old.is_arch == 'Действующий':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'В архиве'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' архивирован',
                          'archived': 1})
            db.session.commit()
            return redirect(url_for('all'))
        if old.is_arch == 'В архиве':
            to_changes = Contract.query.filter_by(id=set.id.data).update({'is_arch': 'Действующий'})
            deals.append({'id': set.id.data,
                          'name': str(old.number) + ' задействован',
                          'archived': 2})
            db.session.commit()
            return redirect(url_for('all'))

    if history_clear.validate_on_submit() and history_clear.clear.data:
        print('Deals have been cleared')
        deals.clear()

    if history_cancel.validate_on_submit and history_cancel.cancel.data:
        i = 0
        for deal in deals:
            if deal['id'] == history_cancel.id.data:
                if deal['archived'] == 1:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'Действующий'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('all'))
                elif deal['archived'] == 2:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'is_arch': 'В архиве'})
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('all'))
                else:
                    to_changes = Contract.query.filter_by(id=deal['id']).update({'paid': deal['old_paid'], 'date': deal['old_date']})
                    print(deal['old_paid'])
                    print(deal['old_date'])
                    db.session.commit()
                    deals.pop(i)
                    return redirect(url_for('all'))
            i += 1

    if search.validate_on_submit() and search.search.data:
        searched = get_contracts_by_id(search.search.data)
        status_active = 'activated'
        bcg_stat = 'search_bcg_active'

    if search_close.validate_on_submit() and search_close.close.data:
        status_active = 'q'
        bcg_stat = 'q'

    return render_template('unpaid.html', contracts=contracts, set=set, archive=archive, nav=nav,
                           history_clear=history_clear, deals=deals, history_cancel=history_cancel, search = search, searched = searched, status_active = status_active, search_close = search_close, bcg_stat=bcg_stat)


@app.route('/test', methods=['GET', 'POST'])
def test():
    test_one = Test_one()
    test_two = Test_two()
    nav = ['Архив', [['Лист неоплативших', '/unpaid'], ['Добавить договор', '/add-user']]]

    if test_one.validate_on_submit() and test_one.add.data:
        print('one')

    if test_two.validate_on_submit() and test_two.sub.data:
        print('two')

    return render_template('test.html', test_one=test_one, test_two=test_two, nav=nav)
