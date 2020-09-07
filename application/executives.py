from flask import render_template, Blueprint, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from markupsafe import Markup

from .models import customerAccount , Customer
from . import db
from datetime import datetime

executives = Blueprint('executives', __name__)
login = 1


# customer form added with regex
# frontend completed for create customer
@executives.route('/create-customer')
@login_required
def create_customer():
    if current_user.is_executive():
        return render_template('executive/customer/create.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


# route for processing customer creation
@executives.route('/addcust', methods=['GET', 'POST'])
@login_required
def addcust():
    # print("Hello")
    if request.method == 'POST':
        ssn_id = request.form['ssn_id']
        cust_name = request.form['cust_name']
        age = request.form['age']
        addr = request.form['addr']
        stateSelect = request.form['stateSelect']
        citySelect = request.form['citySelect']

        new_cust = Customer(ssn=ssn_id, custName=cust_name, age=age, addr=addr,
                            stateSelect=stateSelect, citySelect=citySelect)

        db.session.add(new_cust)
        db.session.commit()

        allcust = Customer.query.all()

        return redirect(url_for('executives.customer_status'))
    else:
        return redirect(url_for('executives.create_customer'))

#search for update
@executives.route('/searchfup',methods=['GET','POST'])
@login_required
def search_update():
    if current_user.is_executive():
        return render_template('executive/customer/sfupdate.html',login=login)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))



@executives.route('/update-customer', methods=['GET', 'POST'])
@login_required
def update_customer():
    if request.method == 'POST':
        ssn = request.form.get('ssn_id')
        # print(ssn)
        a = Customer.query.all()
        # print(a)
        sl = []
        for cust in a:
            sl.append(cust.ssn)
        # print(sl)
        if int(ssn) in sl:
            # print(ssn)
            sfu = Customer.query.filter_by(ssn=ssn).first()
            return render_template('executive/customer/update.html', login=login, sfu=sfu)
        else:
            return render_template('executive/customer/sfupdate.html', login=login)
    else:
        return render_template('executive/customer/sfupdate.html', login=login)


# route for edit the customer data
@executives.route('/editcust', methods=['GET', 'POST'])
@login_required
def edit_cust():
    if request.method == 'POST':
        # cname=print(request.form.get('cust_new_name'))
        # caddr=print(request.form.get('cust_new_addr'))
        # cage=print(request.form.get('cust_new_age'))
        # cid(request.form.get('cust_id'))

        id = request.form.get('cust_id')
        ssn = request.form.get('cust_ssnid')
        print(ssn)
        cust = Customer.query.filter_by(ssn=ssn).first()
        print(cust)
        cust.custName = request.form.get('cust_new_name')
        cust.addr = request.form.get('cust_new_addr')
        cust.age = request.form.get('cust_new_age')
        db.session.commit()
        return redirect(url_for('executives.customer_status'))
    else:
        return redirect(url_for('executives.update_customer'))


@executives.route('/delete-customer', methods = ["GET", "POST"])
@login_required
def delete_customer():
    print("Hello Delete")
    if current_user.is_executive():
        if request.method == 'POST':
            print("Hello")
            #print(request.form.get('cust_ssn'))
            # print(request.form.get('cust_name'))
            # print(request.form.get('cust_addr'))
            # print(request.form.get('cust_age'))
            ssn = request.form.get('cust_ssn')
            print(ssn)
            cust = Customer.query.filter_by(ssn=ssn).first()
            # print(cust)
            if int(request.form.get('cust_ssn')) == cust.ssn and request.form.get('cust_name') == cust.custName and request.form.get('cust_addr') == cust.addr and int(
                    request.form.get('cust_age')) == cust.age:
                db.session.delete(cust)
                db.session.commit()

                return redirect(url_for('executives.customer_status'))
            else:
                return render_template('executive/customer/delete.html', login=login)

        else:
            return render_template('executive/customer/delete.html', login=login)


    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administratoer if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))

#route for customer status.html file
@executives.route('/customer-status')
@login_required
def customer_status():
    if current_user.is_executive():
        allcust = Customer.query.all()
        return render_template('executive/customer/status.html',login = login, cust=allcust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@executives.route('/search-customer', methods=['GET', 'POST'])
@login_required
def search_customer():
    if current_user.is_executive():
        # dummy()
        cid = request.form.get('search_cust_id')
        aid = request.form.get('search_acc_id')
        cust = None
        if cid:
            cust = customerAccount.query.filter_by(id=cid).first()
        elif aid:
            cust = customerAccount.query.filter_by(aid=aid).first()
        if cust:
            print(cust.status)
            return render_template('cashier/account_detail.html', cust=cust)

        return render_template('cashier/account_detail.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@executives.route('/customer-profile-<cid>')
@login_required
def customer_profile(cid):
    if current_user.is_executive():
        allcust = Customer.query.get_or_404(cid)
        return render_template('executive/customer/customer_detail.html', login=login, profile=allcust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))

#Crud operation for acount:

# account form added with regex
# frontend completed for create account
@executives.route('/create-account')
@login_required
def create_account():
    if current_user.is_executive():
        return render_template('executive/account/create.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


# route f0r creating acount processing
@executives.route('/addaccount', methods=['POST', 'GET'])
@login_required
def add_account():
    if request.method == 'POST':
        ssn = request.form.get('ssn_id')
        # print(ssn)
        cust = Customer.query.all()
        # print(cust)
        slist = []
        for c in cust:
            slist.append(c.ssn)
        # print(slist)
        if int(ssn) in slist:
            reqcust = Customer.query.filter_by(ssn=ssn).first()
            # print(reqcust)
            reqcust.atype = request.form.get('acc_type')
            # print(datetime.now)
            a = datetime.now()
            reqcust.alastUpdated = a
            reqcust.balance = request.form.get('deposit_amt')
            db.session.commit()
        print('successfull')
        return redirect(url_for('executives.account_status'))

    return redirect(url_for('executives.create_account'))


@executives.route('/delete-account')
@login_required
def delete_account():
    if current_user.is_executive():
        allcust = Customer.query.all()
        return render_template('executive/account/delete.html', login=login, cust = allcust)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))

#route for processing dlt
@executives.route('/del-account',methods=['POST','GET'])
@login_required
def del_account():
    if request.method=='POST':
        ssn=request.form.get('cust_snid')
        print(ssn)
        cust=Customer.query.filter_by(ssn=ssn).first()
        cust.atype=''
        cust.balance=''

        cust.alastUpdated=datetime.now()
        db.session.commit()
        return redirect(url_for('executives.account_status'))
    else:

        return redirect(url_for('executives.delete_account'))


@executives.route('/account-status')
@login_required
def account_status():
    if current_user.is_executive():
        allcust = Customer.query.all()
        return render_template('executive/account/status.html', login=login, cust=allcust)

    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@executives.route('/search-account')
@login_required
def search_account():
    if current_user.is_executive():
        return render_template('executive/account/search.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


def dummy():
    customer = customerAccount(id=1, ssn=987654321, aid=123789456, atpye=0, status='Active', msg=None)
    db.session.add(customer)
    db.session.commit()
