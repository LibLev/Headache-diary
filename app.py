from flask import Flask, render_template, redirect, session, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from database import queries
import hash

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

s = URLSafeTimedSerializer('Thisisasecret!')


@app.route('/', methods=['GET', 'POST'])
def main_page():
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
        token = s.dumps(email, salt='email-confirm')

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
            email = s.loads(token, salt='email-confirm', max_age=86400)
        except SignatureExpired:
            return render_template('confirmation.html', status='not_valid')
        return redirect('/login')
    return render_template('confirmation.html', status='valid')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = queries.get_user(request.form.get('username'))
        password = request.form.get('password')
        verified = hash.verify_password(password, user[1])
        if verified:
            session['username'] = user[0]
            session['is_valid'] = True
        return render_template('index.html')


def get_registration_data():
    user_name = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    e_mail_address = request.form.get('email_address')
    password = hash.hash_password(request.form.get('password'))
    return user_name, first_name, last_name, password, e_mail_address


if __name__ == '__main__':
    app.run()
