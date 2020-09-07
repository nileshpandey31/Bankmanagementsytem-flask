from flask import render_template, Blueprint, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from markupsafe import Markup

from . import db
from .models import Transaction, Customer
from application.models import customerAccount
import datetime
from sqlalchemy import func
import pdfkit
from flask import make_response


cashier = Blueprint('cashier', __name__)


@cashier.route('/accounts-operation')
@login_required
def account_detail():
    if current_user.is_cashier():
        return render_template('cashier/account_detail.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


'''
@cashier.route('/deposit-money')
@login_required
def deposit():
    #cust = customerAccount.query.filter_by(id=cust_data).first()
    return render_template('cashier/deposit.html', cust='')
'''


@cashier.route('/deposit-money-<cust_data>', methods=['GET', 'POST'])
@login_required
def deposit(cust_data):
    if current_user.is_cashier():
        cust = Customer.query.filter_by(cid=cust_data).first()
        return render_template('cashier/deposit.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/transfer-money-<cust_data>', methods=['GET', 'POST'])
@login_required
def transfer(cust_data):
    if current_user.is_cashier():
        cust = Customer.query.filter_by(cid=cust_data).first()
        return render_template('cashier/transfer.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/withdraw-money-<cust_data>', methods=['GET', 'POST'])
@login_required
def withdraw(cust_data):
    if current_user.is_cashier():
        cust = Customer.query.filter_by(cid=cust_data).first()
        return render_template('cashier/withdraw.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/get-statements')
@login_required
def statements():
    if current_user.is_cashier():
        return render_template('cashier/statements.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/statements', methods=['GET', 'POST'])
@login_required
def get_statements():
    if current_user.is_cashier():
        # dummy()
        id = request.form.get('acc_id')
        tran = request.form.get('transaction_type')
        no = request.form.get('num_of_t')
        sd = request.form.get('start_date')
        ed = request.form.get('end_date')
        print(id, tran, no, sd, ed)
        if sd and ed and tran == "Start and end date" and no:
            # sc = Transaction.query.filter(func.DATE(Transaction.dt) >= sd, func.DATE(Transaction.dt) <= ed, Transaction.cid == id ).count()
            s = Transaction.query.filter(func.DATE(Transaction.dt) >= sd, func.DATE(Transaction.dt) <= ed,
                                         Transaction.cid == id).order_by(Transaction.Tid.desc()).limit(no)
            if s:
                for i in s:
                    print(i.cid, i.dt)
                ren = render_template('cashier/stat.html', s=s)
                pdf = pdfkit.from_string(ren, False)
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'inline; filename = statement.pdf'
                return response

        elif sd and ed and tran == "Start and end date":
            s = Transaction.query.filter(func.DATE(Transaction.dt) >= sd, func.DATE(Transaction.dt) <= ed,
                                         Transaction.cid == id).order_by(Transaction.Tid.desc())
            if s:
                for i in s:
                    print(i.cid, i.dt)
                ren = render_template('cashier/stat.html', s=s)
                pdf = pdfkit.from_string(ren, False)
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'inline; filename = statement.pdf'
                return response

        elif not sd and not ed and tran == "Last transactions" and no:
            s = Transaction.query.filter(Transaction.cid == id).order_by(Transaction.Tid.desc()).limit(no)
            if s:
                for i in s:
                    print(i.cid, i.dt)
                ren = render_template('cashier/stat.html', s=s)
                pdf = pdfkit.from_string(ren, False)
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'inline; filename = statement.pdf'
                return response

        elif not sd and not ed and tran == "Last transactions":
            s = Transaction.query.filter(Transaction.cid == id).order_by(Transaction.Tid.desc())
            if s:
                for i in s:
                    print(i.cid, i.dt)
                ren = render_template('cashier/stat.html', s=s)
                pdf = pdfkit.from_string(ren, False)
                response = make_response(pdf)
                response.headers['content-Type'] = 'application/pdf'
                response.headers['content-Disposition'] = 'inline; filename = statement.pdf'
                return response

        return render_template('cashier/statements.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/deduct-<cust_data>', methods=['GET', 'POST'])
@login_required
def deduct(cust_data):
    if current_user.is_cashier():
        wamt = request.form.get('wamt')
        print(wamt)
        print(cust_data)
        cust = Customer.query.filter_by(cid=cust_data).first()
        # cust.balance = 10000
        # db.session.commit()
        if int(cust.balance) >= int(wamt) and int(cust.balance) > 0 and int(wamt) > 0:
            cust.balance = int(cust.balance) - int(wamt)
            db.session.commit()
            Trans = Transaction(cid = cust.ssn, type = "Withdraw", wamt = wamt, bal = cust.balance)
            db.session.add(Trans)
            db.session.commit()
            return render_template('cashier/account_detail.html', cust=cust)

        return render_template('cashier/withdraw.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/add-<cust_data>', methods=['GET', 'POST'])
@login_required
def add(cust_data):
    if current_user.is_cashier():
        wamt = request.form.get('wamt')
        print(wamt)
        print(cust_data)
        cust = Customer.query.filter_by(cid=cust_data).first()
        # cust.balance = 10000
        # db.session.commit()
        print(cust.atype)
        if int(wamt) > 0:
            cust.balance = int(cust.balance) + int(wamt)
            db.session.commit()
            Trans = Transaction(cid=cust.ssn, type="Deposit", wamt=wamt, bal=cust.balance)
            db.session.add(Trans)
            db.session.commit()
            return render_template('cashier/account_detail.html', cust=cust)

        return render_template('cashier/deposit.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@cashier.route('/transfercust-<cust_data>', methods=['GET', 'POST'])
@login_required
def transfercust(cust_data):
    if current_user.is_cashier():
        wamt = request.form.get('wamt')
        tarid = request.form.get('tar_id')
        type = request.form.get('t_acc_type')
        cust = Customer.query.filter_by(cid=cust_data).first()
        tar = Customer.query.filter_by(ssn=tarid).first()


        if tar and int(cust.balance) > 0 and int(cust.balance) >= int(wamt) and int(cust.cid) != int(
                tar.cid) and type == cust.atype and int(wamt) > 0:
            cust.balance = int(cust.balance) - int(wamt)
            tar.balance = int(tar.balance) + int(wamt)
            db.session.commit()
            Trans = Transaction(cid=cust.ssn, type="Withdraw", wamt=wamt, bal=cust.balance, To_account  = tar.ssn)
            db.session.add(Trans)
            db.session.commit()
            Trans = Transaction(cid=tar.ssn, type="Deposit", wamt=wamt, bal=tar.balance, To_account=cust.ssn)
            db.session.add(Trans)
            db.session.commit()
            return render_template('cashier/account_detail.html', cust=cust)

        return render_template('cashier/transfer.html', cust=cust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


'''
def dummy():
    t = Transaction(cid = 12345, type = "Deposit", dt = datetime.datetime(2020,5,17,10,10,10))
    t1 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 18, 10, 10, 10))
    t2 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 19, 10, 10, 10))
    t3 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 20, 10, 10, 10))
    t4 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 21, 10, 10, 10))
    t5 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 22, 10, 10, 10))
    t6= Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 23, 10, 10, 10))
    t7 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 24, 10, 10, 10))
    t8 = Transaction(cid=12345, type="Deposit", dt=datetime.datetime(2020, 5, 25, 10, 10, 10))
    db.session.add(t)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.add(t4)
    db.session.add(t5)
    db.session.add(t6)
    db.session.add(t7)
    db.session.add(t8)
    db.session.commit()
'''