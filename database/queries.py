from database import data_manager


def find_user(u_name):
    return data_manager.execute_dml_statement('''
    select user_name, id
    from users
    where user_name=%(user_name)s''',
                                              variables={'user_name': u_name})


def insert_new_user(u_name, f_name, l_name, pword, email):
    data_manager.execute_dml_statement("""
    insert into users (user_name,first_name,last_name,hashed_password,email_address)
    values (%(user_name)s, %(first_name)s, %(last_name)s, %(hashed_password)s, %(email_address)s)
    """,
                                       variables={'user_name': u_name, 'first_name': f_name, 'last_name': l_name,
                                                  'hashed_password': pword, 'email_address': email})


def get_user(username):
    return data_manager.execute_dml_statement('''
    SELECT user_name, hashed_password, first_name, last_name, email_address, id
    FROM users
    WHERE user_name=%(username)s
    ''', variables={'username': username})


def insert_new_value_at_morning(u_id, value, time):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, morning_scale, submission_time)
    VALUES (%(u_id)s, %(value)s, %(time)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time})


def check_morning_data():
    return data_manager.execute_dml_statement('''
    SELECT user_id, morning_scale, day
    FROM phases''')


def insert_new_value_at_afternoon(u_id, value, time):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, afternoon_scale, submission_time)
    VALUES (%(u_id)s, %(value)s, %(time)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time})


def check_afternoon_data():
    return data_manager.execute_dml_statement('''
    SELECT user_id, afternoon_scale
    FROM phases''')


def insert_new_value_at_evening(u_id, value, time):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, evening_scale, submission_time)
    VALUES (%(u_id)s, %(value)s, %(time)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time})


def check_evening_data():
    return data_manager.execute_dml_statement('''
    SELECT user_id, evening_scale
    FROM phases''')
