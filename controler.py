#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3


#用来处理用Python的sqlite3操作数据库要插入的字符串中含有中文字符的时候报错处理，配合map
def _decode_utf8(aStr):
    return aStr.encode('utf-8','ignore').decode('utf-8')

def create_db():
    '''create a db and table if not exists'''
    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JAVBUS_DATA(
            URL       TEXT PRIMARY KEY,
            cover_image TEXT,
            code_name    TEXT,
            release_date  TEXT,
            duration      TEXT,
            director      TEXT,
            manufacturer    TEXT,
            publisher    TEXT,
            series      TEXT,
            actor      TEXT,
            genre      TEXT,
            magnet  TEXT,
            uncensored      INTEGER);''')

    print("Table created successfully")
    cursor.close()
    conn.commit()
    conn.close()

def write_data(dict_jav, uncensored):
    '''write_data(dict_jav, uncensored)'''

    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()
    #对数据解码为unicode
    insert_data = map(_decode_utf8, (dict_jav['URL'], dict_jav['cover_image'],dict_jav['code_name'], dict_jav['release_date'], dict_jav['duration'], dict_jav['director'], dict_jav['manufacturer'], dict_jav['publisher'], dict_jav['series'], dict_jav['actor'], dict_jav['genre'], dict_jav['magnet']))
    insert_data.append(uncensored)
    #插入数据
    try:
        cursor.execute('''
    INSERT INTO JAVBUS_DATA (URL, cover_image,code_name, release_date, duration, director, manufacturer, publisher, series, actor, genre, magnet, uncensored)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)
    except sqlite3.IntegrityError as e:
        print e
        pass
    cursor.close()
    conn.commit()
    conn.close()

def check_url_not_in_table(url):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""

    conn = sqlite3.connect("javbus.sqlite3.db")
    cursor = conn.cursor()

    cursor.execute('select URL from JAVBUS_DATA where URL=?', (url.decode('utf-8'),))
    check = cursor.fetchall()
    cursor.close()
    conn.close()
    if check:
        return False
    return True