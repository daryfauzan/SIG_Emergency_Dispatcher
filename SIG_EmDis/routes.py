from flask import render_template, url_for, flash, redirect, request
from SIG_EmDis import app, db
from SIG_EmDis.forms import LoginForm

@app.route('/', methods=["POST","GET"])
@app.route('/login', methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')