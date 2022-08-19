import os

import pandas
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from .models import Expense

views = Blueprint('views', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/statement', methods=['GET', 'POST'])
@login_required
def statement():
    if request.method == 'POST':
        # file = request.form.get('file')
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(url_for('statement'))

        file = request.files['file']
        print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(UPLOAD_FOLDER, filename))

            food_companies = ['KAUFLAND', 'BILLA', 'LIDL', 'BOLERO', 'ANET']  # companie names to check for Groceries
            petrol_companies = ['BI OIL', 'DEGA', 'LUKOIL', 'EKO',
                                "SHELL", ]  # companie names to check for Gas Expenses

            data = pandas.read_excel(file, sheet_name='Sheet')

            df = pandas.DataFrame(data)
            food_exp = 0
            gas_exp = 0
            withdraw_exp = 0
            other_exp = 0



            food_values = []

            gas_values = []
            other_values = []
            food_dates = []
            gas_dates = []
            other_dates = []

            for i in range(9, len(df)):

                gas, food, draw = False, False, False

                draw_col = df.loc[i][5]  # COLUMN from table to get payment method

                if type(draw_col) != float and type(
                        df.loc[i][7]) != float:  # if statement to check for withdraw from ATM
                    if 'ATM' in draw_col:
                        withdraw_exp += float(df.loc[i][3])
                        draw = True

                if type(df.loc[i][7]) != float:  # if statement to check for Gas expenses using petrol list
                    for element in petrol_companies:
                        if element in df.loc[i][7]:
                            gas_exp += float(df.loc[i][3])
                            gas = True
                            gas_values.append(float(df.loc[i][3]))
                            gas_dates.append(str(df.loc[i][2]))

                if type(df.loc[i][7]) != float:  # if statement to check for Grocerie expenses using Grocerie list
                    for element in food_companies:
                        if element in df.loc[i][7]:
                            food_exp += float(df.loc[i][3])
                            food = True

                            food_values.append(float(df.loc[i][3]))
                            food_dates.append(str(df.loc[i][2]))


                if not gas and not food and not draw:  # if Expense is not in above statements
                    if str(df.loc[i][3]) != 'nan':
                        other_exp += float(df.loc[i][3])
                        other_values.append(float(df.loc[i][3]))
                        other_dates.append(str(df.loc[i][2]))
                        # print(float(df.loc[i][3]), df.loc[i][7])



            return render_template('statement.html',
                                   user=current_user,
                                   food_exp=round(food_exp,2),
                                   food_values=food_values,
                                   gas_exp=round(gas_exp,2),
                                   gas_values=gas_values,
                                   other_values=other_values,
                                   other_exp=round(other_exp,2),
                                   food_dates=food_dates,
                                   )

    return render_template('statement.html', user=current_user)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense_name = request.form.get('expense_name')
        expense_amount = request.form.get('expense_amount')
        expense_date = request.form.get('expense_date')

        if len(expense_name) < 1:
            flash('Expense is empty', category='error')
        elif len(expense_amount) < 1:
            flash('Amount is empty', category='error')
        elif float(expense_amount) <= 0:
            flash('Expense is can\'t be less than or equal to 0', category='error')
        elif type(float(expense_amount)) != float and type(int(expense_amount)) != int:
            flash('Please enter a number!', category='error')
        else:
            new_expense = Expense(expense_name=expense_name, expense_amount=expense_amount, expense_date=expense_date, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added', category='success')

    query = Expense.query.all()
    total = 0
    for expense in query:
        if expense.user_id == current_user.id:
            total += float(expense.expense_amount)

    return render_template('home.html', user=current_user, total=round(total, 3))


@views.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):

    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted', category='success')

    return redirect(url_for('views.home'))
