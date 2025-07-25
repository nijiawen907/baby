import sqlite3
import threading

# 使用线程本地存储
db_local = threading.local()


def get_db_connection():
    """获取当前线程的数据库连接"""
    if not hasattr(db_local, 'conn'):
        db_local.conn = sqlite3.connect('scene.db')
    return db_local.conn


def get_db_cursor():
    """获取当前线程的数据库游标"""
    conn = get_db_connection()
    if not hasattr(db_local, 'cursor'):
        db_local.cursor = conn.cursor()
    return db_local.cursor


# 创建表（线程安全版）
def create_table():
    cursor = get_db_cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scene_img (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        status TEXT NOT NULL,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    get_db_connection().commit()


# 插入数据（线程安全版）
def insert_scene(image_path, status):
    cursor = get_db_cursor()
    cursor.execute('''
    INSERT INTO scene_img (image_path, status)
    VALUES (?, ?)
    ''', (image_path, status))
    get_db_connection().commit()
    return cursor.lastrowid


# 查询数据（线程安全版）
def get_all_scenes():
    cursor = get_db_cursor()
    cursor.execute('SELECT * FROM scene_img')
    return cursor.fetchall()


# 获取happy
def get_happy_scenes():
    cursor = get_db_cursor()
    cursor.execute('''
    SELECT * FROM scene_img
    WHERE status = (?)
    ''', ("Happy",))
    return cursor.fetchall()


def get_last_scene():
    cursor = get_db_cursor()
    cursor.execute('''
    SELECT * FROM scene_img 
    ORDER BY id DESC 
    LIMIT 1
    ''')
    return cursor.fetchone()


# 关闭连接（每个线程需单独调用）
def close_connection():
    if hasattr(db_local, 'conn'):
        db_local.conn.close()
        del db_local.conn
    if hasattr(db_local, 'cursor'):
        del db_local.cursor


if __name__ == '__main__':
    create_table()