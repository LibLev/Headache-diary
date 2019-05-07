from database import data_manager


def test():
    return data_manager.execute_select('''
    SELECT id FROM users
    ''')

