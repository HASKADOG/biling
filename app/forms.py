from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired

class Contract_add(FlaskForm):
    number = StringField('Number', validators=[DataRequired()])
    is_arch = StringField('Status')
    date = IntegerField('День списания')
    paid = IntegerField('Кол-во оплаченных месяцев')
    submit = SubmitField('Добавить')

class Set_paid(FlaskForm):
    id = IntegerField('')
    paid = IntegerField('Кол-во мес.')
    date = IntegerField('День списания')
    submit = SubmitField('Продлить')

class Archive(FlaskForm):
    id = IntegerField('')
    add = SubmitField('В архив')

class Test_one(FlaskForm):
    add = SubmitField('')

class Test_two(FlaskForm):
    sub = SubmitField('')

class History_clear(FlaskForm):
    clear = SubmitField('')

class History_cancel(FlaskForm):
    id = IntegerField('')
    cancel = SubmitField('')

class Search(FlaskForm):
    search = StringField('')
    go = SubmitField('')

class Search_close(FlaskForm):
    close = SubmitField('')

class Delete_contract(FlaskForm):
    idd = IntegerField('')
    delete = SubmitField('')
