from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from SIG_EmDis import app, db
from SIG_EmDis.forms import LoginForm
from SIG_EmDis.models import Dispatcher

@app.route('/', methods=["POST","GET"])
@app.route('/login', methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Dispatcher.query.filter_by(email=form.email.data).first()
        if user and form.password.data == user.password:
            user.isOnline = True
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash("Your email or password is wrong", "danger")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = Dispatcher.query.filter_by(email=current_user.email)
    user.isOnline = False
    db.session.commit()
    return render_template('dashboard.html')