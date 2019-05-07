from flask import Flask, render_template, redirect, session, request
from database import queries
import hash

app = Flask(__name__)


@app.route('/')
def hello_world():

    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username, first_name, last_name, password, email = get_registration_data()
        check_name = queries.find_user(u_name=username)
        if check_name['user_name'] is not None:
            return render_template('registration.html',
                                   message='Sorry, This user name is already in use. Please Select another')
        queries.insert_new_user(u_name=username, f_name=first_name, l_name=last_name, pword=password, email=email)
        return redirect('/')
    return render_template('registration.html')


def get_registration_data():
    user_name = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    e_mail_address = request.form.get('email_address')
    password = hash.hash_password(request.form.get('password'))
    return user_name, first_name, last_name ,password, e_mail_address


if __name__ == '__main__':
    app.run()
