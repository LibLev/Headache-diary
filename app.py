from flask import Flask, render_template, redirect, session, request
from database import queries
import hash
from time import strftime, localtime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/index')
def index():
    if session.get('username') is None:
        return redirect('/')
    dayPhase()
    return render_template('index.html', dayPhase=dayPhase())


@app.route('/')
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
        return redirect('/')
    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = queries.get_user(request.form.get('username'))
        password = request.form.get('password')
        verified = hash.verify_password(password, user[1])
        if verified:
            session['username'] = user[0]
            session['first_name'] = user[2]
            session['last_name'] = user[3]
            session['email'] = user[4]
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
        scale = request.form.get('optradio')
    return redirect('/index')


def dayPhase():
    month_day = strftime('%m.%d', localtime())
    hour_minute = strftime('%H:%M', localtime())
    current_date_and_time = month_day+'.'+hour_minute
    get_time = hour_minute.split(':')
    if int(get_time[0]) >= 0 and int(get_time[0]) < 11:
        currentPhase = 'morning'
    elif int(get_time[0]) >= 11 and int(get_time[0]) < 17:
        currentPhase = 'afternoon'
    elif int(get_time[0]) >= 17 and int(get_time[0]) < 23:
        currentPhase = 'evening'

    return currentPhase




if __name__ == '__main__':
    app.run()
