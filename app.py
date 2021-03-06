from flask import Flask, render_template, redirect, session, request, url_for, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from database import queries
import hash
from time import strftime, localtime
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USERNAME='headachediary.noreply@gmail.com',
    MAIL_PASSWORD='cheeseCake02',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False
)

mail = Mail(app)

secret = URLSafeTimedSerializer('Thisisasecret!')


@app.route('/index')
def index():
    if session.get('username') is None:
        return redirect('/')
    try:
        current_day = queries.get_last_day(session.get('user_id'))[0]
    except TypeError:
        current_day = None
        queries.bind_user_to_phase(session.get('user_id'), datetime.datetime.now())
    day_phase_is_done = False

    try:
        usr_id = session['user_id']
        if day_phase() is 'morning':
            # next_day = queries.check_evening_data(usr_id)[0]
            # if next_day is not None:
            #     queries.set_next_day(usr_id, queries.get_last_day(usr_id)[0] + 1)

            data = queries.check_morning_data(usr_id)
            if data[0] is None:
                day_phase_is_done = False
        elif day_phase() is 'afternoon':
            data = queries.check_afternoon_data(usr_id)
            if data[1] is None:
                day_phase_is_done = False
        elif day_phase() is 'evening':
            data = queries.check_evening_data(usr_id)
            if data[2] is None:
                day_phase_is_done = False
    except IndexError:
        day_phase_is_done = False
    return render_template('index.html', dayPhase=day_phase(), current_day=current_day,
                           dayPhaseIsDone=day_phase_is_done)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if session.get('username'):
        return redirect('/index')
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username, first_name, last_name, password, email = get_registration_data()
        check_name = queries.find_user(username)
        if check_name is not None:
            return render_template('registration.html',
                                   message='Sorry, This user name is already in use. Please Select another')
        queries.insert_new_user(username, first_name, last_name, password, email)
        token = secret.dumps(email, salt='email-confirm')

        msg = Message('Registration confirmation(do not reply!)', sender='headachediary.noreply@gmail.com',
                      recipients=[email])

        link = url_for('confirmation', token=token, _external=True)

        msg.body = '''Dear {}, 
        
        Thank you very much for your registration
        Your confirmation link is: {}
        
        Best regards,
        
        Headache Diary ltd.
        
        !!!Please DO NOT reply!!!'''.format(username, link)

        mail.send(msg)
        return redirect('/')
    return render_template('registration.html')


@app.route('/confirmation/<token>', methods=['GET', 'POST'])
def confirmation(token):
    if request.method == 'POST':
        try:
            email = secret.loads(token, salt='email-confirm', max_age=86400)
        except SignatureExpired:
            return render_template('confirmation.html', status='not_valid')
        return redirect('/login')
    return render_template('confirmation.html', status='valid')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = queries.get_user(request.form.get('username'))
        if user is None:
            return redirect('/')
        password = request.form.get('password')
        verified = hash.verify_password(password, user[1])
        if verified:
            session['username'] = user[0]
            session['first_name'] = user[2]
            session['last_name'] = user[3]
            session['email'] = user[4]
            session['user_id'] = user[5]
            session['is_valid'] = True
        return redirect('/index')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/')


def get_registration_data():
    user_name = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    e_mail_address = request.form.get('email_address')
    password = hash.hash_password(request.form.get('password'))
    return user_name, first_name, last_name, password, e_mail_address


@app.route('/scale', methods=['POST', 'GET'])
def scale():
    if request.method == 'POST':
        last_day = queries.get_last_day(session.get('user_id'))[0]

        if day_phase() == 'morning':
            user_id = session.get('user_id')
            value = request.form.get('optradio')
            time = datetime.datetime.now()
            queries.insert_new_value_at_morning(user_id, value, time, last_day)
        elif day_phase() == 'afternoon':
            user_id = session.get('user_id')
            value = request.form.get('optradio')
            time = datetime.datetime.now()
            queries.insert_new_value_at_afternoon(user_id, value, time, last_day)
        elif day_phase() == 'evening':
            user_id = session.get('user_id')
            value = request.form.get('optradio')
            time = datetime.datetime.now()
            queries.insert_new_value_at_evening(user_id, value, time, last_day)
    return redirect('/index')


def day_phase():
    month_day = strftime('%m.%d', localtime())
    hour_minute = strftime('%H:%M', localtime())
    current_date_and_time = month_day + '.' + hour_minute
    get_time = hour_minute.split(':')
    if int(get_time[0]) >= 0 and int(get_time[0]) < 11:
        currentPhase = 'morning'
    elif int(get_time[0]) >= 11 and int(get_time[0]) < 17:
        currentPhase = 'afternoon'
    elif int(get_time[0]) >= 17 and int(get_time[0]) < 23:
        currentPhase = 'evening'
    elif int(get_time[0]) >= 23 and int(get_time[1]) < 59:
        currentPhase = 'evening'

    return currentPhase


@app.route('/start_diary', methods=['GET'])
def start_diary():
    queries.start_diary_day(session.get('user_id'))
    return redirect('/index')


@app.route('/api/day-scales', methods=['GET'])
def get_tasks():
    day_scales = queries.get_day_scales(session.get('user_id'))
    return jsonify({'day_scales': day_scales})


if __name__ == '__main__':
    app.run()
