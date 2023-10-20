import sqlite3


def add_user(id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO userTypes (id, type) VALUES (?, 0)
    ''', (id,))
    connection.commit()
    connection.close()


def get_user_type(person_id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT type FROM userTypes WHERE id=?
    ''', (person_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def set_user_type(person_id, type):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE userTypes SET type=? WHERE id=?
    ''', (type, person_id))
    connection.commit()
    connection.close()


def add_question(id, quest, m_id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO questions (message_id, id, question, answer, isAnswered) VALUES (?, ?, ?, "", 0)
    ''', (m_id, id, quest,))
    connection.commit()
    connection.close()


def get_question():
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
            SELECT message_id, id, question FROM questions WHERE isAnswered=?
        ''', (0,))
    result = cursor.fetchone()
    connection.close()
    return result


def set_question_answer(m_id, answer):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE questions SET answer=?, isAnswered=? WHERE message_id=?
    ''', (answer, 1, m_id,))
    connection.commit()
    connection.close()


def set_current_answerer(m_id, id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE userTypes SET curr_question=? WHERE id=?
    ''', (m_id, id,))
    connection.commit()
    connection.close()


def get_question_author(m_id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                SELECT id FROM questions WHERE message_id=?
            ''', (m_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_message_from_answerer(id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                SELECT curr_question FROM userTypes WHERE id=?
            ''', (id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_by_id(id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                SELECT id, type FROM userTypes WHERE id=?
            ''', (id,))
    result = cursor.fetchone()
    connection.close()
    return result


def get_all_admins():
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                    SELECT id FROM userTypes WHERE type=?
                ''', (404,))
    result = cursor.fetchall()
    connection.close()
    return result


def get_message_id_by_text(message):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                        SELECT message_id FROM questions WHERE question=?
                    ''', (message,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_text_by_message(id):
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                        SELECT question FROM questions WHERE message_id=?
                    ''', (id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_last_q_number():
    connection = sqlite3.connect('datab.db')
    cursor = connection.cursor()
    cursor.execute('''
                            SELECT count(*) FROM questions
                        ''')
    result = cursor.fetchone()
    connection.close()
    return int(result[0])
