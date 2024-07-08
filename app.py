from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm, ResetPasswordForm
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample users
users = {'test@naver.com': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data
        if user_email in users and users[user_email]['password'] == user_password:
            user = User()
            user.id = user_email
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data
        if user_email not in users:
            users[user_email] = {'password': user_password}
            flash('Account created successfully.')
            return redirect(url_for('login'))
        else:
            flash('Email is already registered.')
    return render_template('register.html', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_email = form.email.data
        if user_email in users:
            # Here you should send the reset password email
            flash('Password reset email sent.')
        else:
            flash('Email not found.')
    return render_template('reset_password.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to your dashboard, ' + current_user.id

if __name__ == '__main__':
    app.run(debug=True)