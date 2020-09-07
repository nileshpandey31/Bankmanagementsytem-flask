from flask import render_template, Blueprint, request, redirect, url_for, abort, flash, session
from flask_login import current_user, login_required
from markupsafe import Markup

from application import db
from application.models import User

unauth_routes = Blueprint('routes', __name__)


# when user is authenticated
@unauth_routes.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('routes.login'))

    # edit login='val' to see navbar change val in ['False','cashier','executive']


@unauth_routes.route('/login')
def login():
    add_admin()
    if current_user.is_authenticated:
       message = Markup('Already logged in')
       flash(message, 'warning')
       return redirect(url_for('routes.index'))
    return render_template('auth/login.html')


# All Admin routes below
@unauth_routes.route('/register')
@login_required
def register():
    #add_admin()
    if current_user.is_admin():
        return render_template('auth/admin/register.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect('/')


@unauth_routes.route('/all-users')
@login_required
def user_detail():
    if current_user.is_admin():
        return render_template('auth/admin/user_detail.html')
    flash('Error occured please try again later')
    return redirect(url_for('routes.index'))


@unauth_routes.route('/update-user-<user_data>', methods=['GET', 'POST'])
@login_required
def update_user(user_data):
    if current_user.is_admin():
        user = User.query.filter_by(id=user_data).first()
        return render_template('auth/admin/update_user.html', user=user)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@unauth_routes.route('/update-user-post-<user_data>', methods=['GET', 'POST'])
@login_required
def update_user_post(user_data):
    if current_user.is_admin():
        user = User.query.filter_by(id=user_data).first()
        print(user.name)
        try:
            new_name = request.form.get('new_name')
            new_email = request.form.get('new_email')
            print(new_email, new_name)
            if new_name:
                user.name = new_name
            if new_email:
                user.email = new_email
        except:
            flash('Error occurred')
            return redirect(url_for('routes.all_users'))
        db.session.commit()
        return render_template('auth/admin/all_users.html')
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


@unauth_routes.route('/get-users', methods=['GET', 'POST'])
@login_required
def all_users():
    if current_user.is_admin():
        user = User.query.all()
        return render_template('auth/admin/all_users.html', all_users=user)
    else:
        message = Markup("Error: Not authenticated to perform action.<br /> Contact Administrator if this is a mistake")
        flash(message, 'danger')
        return redirect(url_for('routes.index'))


def add_admin():
    if User.query.count() == 0:
        from werkzeug.security import generate_password_hash
        db.session.add(User(name='administrator', userId='admin', email='admin@xplorebank.com',
                            password=generate_password_hash('admin123', method='sha256'), type=2, aadhar='0'))
        db.session.commit()

