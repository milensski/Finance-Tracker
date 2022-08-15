from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
from .models import Expense
from . import db
import json

views = Blueprint('views', __name__)




@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense_name = request.form.get('expense_name')
        expense_amount = request.form.get('expense_amount')


        if not expense_amount.isnumeric():
            flash('Please enter a number!',category='error')
        elif len(expense_name) < 1:
            flash('Expense is too short',category='error')
        elif len(expense_amount) < 1:
            flash('Expense is too short',category='error')
        elif int(expense_amount) <= 0:
            flash('Expense is can\'t be less than or equal to 0', category='error')
        else:
            new_expense = Expense(expense_name=expense_name,expense_amount=expense_amount,user_id = current_user.id )
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added', category='success')




    return render_template('home.html',user=current_user)


@views.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted', category='success')

    return redirect(url_for('views.home'))