from flask import render_template, url_for, flash, redirect, request, Response
from flask_login import login_user, current_user, logout_user, login_required
from SIG_EmDis import app, db
from SIG_EmDis.forms import LoginForm
from SIG_EmDis.models import Dispatcher, Call, Hospital
import json


def activate_link(link):
    page = {'dashboard':None, 'call_list':None, 'hospital_list':None}
    page[link] = 'active'
    return page

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
    user = Dispatcher.query.filter_by(email=current_user.email)
    user.isOnline = False
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    id = current_user.id
    call = Call.query.filter(Call.pic==id and Call.status != 2)
    return render_template('dashboard.html', title='Dashboard', active_link = activate_link('dashboard'), call=call)

@app.route('/call-list')
@login_required
def call_list():
    id = current_user.id
    call = Call.query.filter(Call.pic==id and Call.status != 2)
    return render_template('call_list.html', title='Call List', active_link = activate_link('call_list'), call=call)

@app.route('/response/<id>')
@login_required
def response(id):
    return render_template('response.html', title='Response Call', id=id, active_link = activate_link('call_list'))

@app.route('/hospital-list')
@login_required
def hospital_list():
    return render_template('hospital_list.html', title='Hospital List', active_link = activate_link('hospital_list'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()

    dis_1 = Dispatcher(name='Dary Fauzan', email='dary@gmail.com', password='dary')
    dis_2 = Dispatcher(name='Annisa Anjani', email='annisa@gmail.com', password='annisa')
    dis_3 = Dispatcher(name='Almandriya', email='alma@gmail.com', password='alma')
    db.session.add(dis_1)
    db.session.add(dis_2)
    db.session.add(dis_3)
    db.session.commit()

    hosp = Hospital(
        name = 'Rumah Sakit Adi Husada Kapasari',
        address = 'Jl. Kapasari No.97-101, Kapasan, Kec. Simokerto, Kota SBY, Jawa Timur 60141',
        phone_num = '(031) 3764555',
        latitude = -7.24255,
        longitude = 112.751865
    )

    db.session.add(hosp)
    db.session.commit()

    return redirect(url_for('login'))



@app.route('/dummy-call', methods=["POST","GET"])
def dummy_call():

    def curr_call(dis):
        return dis[1]

    call_info = {}
    call_info['latitude'] = request.args.get('latitude')
    call_info['longitude'] = request.args.get('longitude')
    call_info['phone_num'] = request.args.get('phone_num')
    call_info['message'] = request.args.get('message')


    online_dis = Dispatcher.query.filter_by(isOnline=True).with_entities(Dispatcher.id, Dispatcher.currCall).all()
    online_dis.sort(key=curr_call)
    least_curr_call = online_dis[0]

    call_info['pic_id'] = least_curr_call[0]

    call = Call(
        latitude = float(call_info['latitude']),
        longitude = float(call_info['longitude']),
        phone_num = call_info['phone_num'],
        message = call_info['message'],
        pic = int(call_info['pic_id']),
        hospital = 1
    )


    pic = Dispatcher.query.filter_by(id=call_info['pic_id']).first()
    pic.currCall += 1

    db.session.add(call)
    db.session.commit()

    return redirect(url_for('login'))
