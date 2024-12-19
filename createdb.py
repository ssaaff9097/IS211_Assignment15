import sqlite3 

db_file = 'blog.db'

create_users_table = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(100) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL
);
"""

create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
content TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id)
);
"""
conn = sqlite3.connect(db_file)
conn.execute(create_users_table)
conn.execute(create_posts_table)
conn.commit()
conn.close()

print("Success!")