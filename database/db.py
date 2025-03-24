import sqlite3

async def create_db() -> None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    topic_id INTEGER,
    serial_number INTEGER,
    email TEXT
    unread_messages_id INT FOREIGN_KEY
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users (id)
    )
  ''')
  db_connection.commit()
  db_connection.close()

async def insert_user(user_id, username = None, serial_number = None, email = None) -> None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute("INSERT INTO users (id, username, serial_number, email) VALUES (?, ?, ?, ?)", (user_id, username, serial_number, email))
  db_connection.commit()
  db_connection.close()

async def insert_message(user_id, message) -> None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (user_id, message))
  db_connection.commit()
  db_connection.close()

async def update_topic(user_id, topic_id) -> None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute("UPDATE users SET topic_id = ? WHERE id = ?", (topic_id, user_id))
  db_connection.commit()
  db_connection.close()

async def update_user_data(user_id, serial_number = None, email = None):
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute("UPDATE users SET serial_number = ?, email = ? WHERE id = ?", (serial_number, email, user_id))
  db_connection.commit()
  db_connection.close()

async def get_user_topic(user_id) -> tuple | None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  res = cursor.execute("SELECT topic_id FROM users WHERE id = ?", (user_id, )).fetchone()
  if res == (None, ):
    res = None
  db_connection.commit()
  db_connection.close()
  return res

async def get_user(user_id) -> tuple | None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  res = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id, )).fetchone()
  if res == (None, ):
    res = None
  db_connection.commit()
  db_connection.close()
  return res

async def get_unread_messages(user_id) -> list | None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  res = cursor.execute("SELECT message FROM messages WHERE user_id = ?", (user_id, )).fetchall()
  if res == [(None, )]:
    res = None
  db_connection.commit()
  db_connection.close()
  return res

async def delete_unread_messages(user_id) -> None:
  db_connection = sqlite3.connect('database/bot.db')
  cursor = db_connection.cursor()
  cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id, ))
  db_connection.commit()
  db_connection.close()