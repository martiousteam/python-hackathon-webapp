# mod_authorization/controllers.py

from flask import request, render_template,  redirect, url_for, Blueprint, flash
from flask_login import login_user, login_required, logout_user
from hackathon.mod_authorization.forms import LoginForm, SignupForm
from hackathon.mod_authorization.models import User

from hackathon import db, app, login_manager


from flask_kerberos import requires_authentication, init_kerberos
init_kerberos(app)

mod_authorization = Blueprint('authorization', __name__, url_prefix='/authorization')


# This flask-login callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
# It should return None (not raise an exception) if the ID is not valid.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@mod_authorization.route("/signup/", methods=["GET", "POST"])
def signup():
    if app.config['ENABLE_KERBEROS']:
        return redirect(url_for('authorization.kerberoslogin'))
    
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        app.logger.info('Signup Attempt, Username = ' + form.username.data + ' Name = ' + form.name.data)
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('authorization.login'))
    return render_template("authorization/signup.html", form=form)

@mod_authorization.route('/logininstructions/')
def logininstructions():
    return render_template('authorization/logininstructions.html')

@mod_authorization.route('/testlogin/')
@login_required
def testlogin():
    return render_template('authorization/testlogin.html')


@mod_authorization.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@mod_authorization.route('/login/', methods=['GET', 'POST'])
def login():

    if app.config['ENABLE_KERBEROS']:
        return redirect(url_for('authorization.kerberoslogin'))

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        # app.logger.info('Login Attempt, Username = ' + login_form.username.data + ' Password = '
        # + login_form.password.data)
        user = User.get_by_username(login_form.username.data)
        # app.logger.info(user)
        if user is not None and user.check_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('codesubmission.participanthome'))
        else:
            flash("Incorrect username and/or password, try again...", "danger")
    return render_template('authorization/login.html', login_form=login_form)


@mod_authorization.route('/kerberoslogin/')
@requires_authentication
def kerberoslogin(user):
    user = User.get_by_kerberosuser(user)
    if user is not None:
        login_user(user)
        return redirect(request.args.get('next') or url_for('codesubmission.participanthome'))
    return redirect(url_for('authorization.unauthorized'))


@mod_authorization.route('/unauthorized/')
def unauthorized():
    return render_template('authorization/unauthorized.html')

