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


def insert_new_value_at_morning(u_id, value, time, num_of_day):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, morning_scale, submission_time, num_of_day)
    VALUES (%(u_id)s, %(value)s, %(time)s, %(num_of_day)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time, 'num_of_day': num_of_day})


def insert_new_value_at_afternoon(u_id, value, time, num_of_day):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, afternoon_scale, submission_time, num_of_day)
    VALUES (%(u_id)s, %(value)s, %(time)s, %(num_of_day)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time, 'num_of_day': num_of_day})


def insert_new_value_at_evening(u_id, value, time, num_of_day):
    return data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, evening_scale, submission_time, num_of_day)
    VALUES (%(u_id)s, %(value)s, %(time)s, %(num_of_day)s)
    ''',
                                              variables={'u_id': u_id, 'value': value,
                                                         'time': time, 'num_of_day': num_of_day})


def check_morning_data(user_id):
    return data_manager.execute_select('''
    SELECT user_id, morning_scale, num_of_day
    FROM phases
    WHERE user_id = %(user_id)s
    ORDER BY num_of_day DESC
    ''', variables={'user_id': user_id})


def check_afternoon_data(user_id):
    return data_manager.execute_dml_statement('''
    SELECT user_id, afternoon_scale, num_of_day
    FROM phases
    WHERE user_id = %(user_id)s
    ORDER BY num_of_day DESC
    ''',
                                              variables={'user_id': user_id})


def check_evening_data(user_id):
    return data_manager.execute_select('''
    SELECT user_id, evening_scale, num_of_day
    FROM phases
    WHERE user_id = %(user_id)s
    ORDER BY num_of_day DESC
    ''',
                                       variables={'user_id': user_id})


def get_last_day(user_id):
    return data_manager.execute_dml_statement('''
    SELECT num_of_day 
    FROM phases
    WHERE user_id = %(user_id)s
    ORDER BY num_of_day DESC
    ''', variables={'user_id': user_id})


def start_diary_day(user_id):
    data_manager.execute_dml_statement('''
    UPDATE phases
    SET num_of_day = 1
    WHERE user_id = %(user_id)s
    ''', variables={'user_id': user_id})


def bind_user_to_phase(user_id, submission_time):
    data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, submission_time)
    VALUES (%(user_id)s, %(submission_time)s)
    ''', variables={'user_id': user_id, 'submission_time': submission_time})


def get_day_scales(user_id):
    return data_manager.execute_select('''
    SELECT num_of_day, array_agg(concat(morning_scale, afternoon_scale, evening_scale)) AS scales
    FROM phases
    WHERE user_id = %(user_id)s
    GROUP BY num_of_day
    ''', variables={'user_id': user_id})


def set_next_day(user_id, day):
    data_manager.execute_dml_statement('''
    INSERT INTO phases(user_id, num_of_day)
    VALUES (%(user_id)s, %(num_of_day)s)
    ''', variables={'user_id': user_id, 'num_of_day': day})
