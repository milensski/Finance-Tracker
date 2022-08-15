from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import Expense

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense_name = request.form.get('expense_name')
        expense_amount = request.form.get('expense_amount')


        if len(expense_name) < 1:
            flash('Expense is empty', category='error')
        elif len(expense_amount) < 1:
            flash('Amount is empty', category='error')
        elif float(expense_amount) <= 0:
            flash('Expense is can\'t be less than or equal to 0', category='error')
        elif type(float(expense_amount)) != float and type(int(expense_amount)) != int:
            flash('Please enter a number!', category='error')
        else:
            new_expense = Expense(expense_name=expense_name, expense_amount=expense_amount, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added', category='success')

    query = Expense.query.all()
    total = 0
    for expense in query:
        if expense.user_id == current_user.id:
            total += float(expense.expense_amount)

    return render_template('home.html', user=current_user, total=round(total,3))


@views.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted', category='success')

    return redirect(url_for('views.home'))
