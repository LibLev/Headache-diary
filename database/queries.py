from database import data_manager


def test():
    return data_manager.execute_select('''
    SELECT id FROM users
    ''')


def find_user(u_name):
    return data_manager.execute_select('''
    select user_name, id
    from users
    where user_name=%(username)s''',
                                       variables={'user_name': u_name})


def insert_new_user(u_name, pword, email, f_name, l_name):
    return data_manager.execute_select("""
    insert into users (user_name,first_name,last_name,hashed_password,email_address)
    values (%(username)s, %(first_name)s, %(last_name)s, %(h_password)s, %(e_mail)s)
    """,
                                       variables={'user_name': u_name, 'first_name': f_name, 'last_name': l_name,
                                                  'hashed_password': pword, 'email_address': email})
