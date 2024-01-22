from forms import UserLoginForm, UserRegistrationForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserRegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data  # 这里应该加密密码

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            # create new user
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)  # 这里应该加密密码
            db.session.add(user)
            db.session.commit()
            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
        else:
            flash('Email already in use', 'error')

    
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You do not have access to this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))