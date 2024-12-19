from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    conn = sqlite3.connect('blog.db')
    return conn

@app.route('/')
def index():
    conn = get_db()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    print("Posts:", posts)  # Debugging line to check what data is being passed to the template
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    print(session)  
    conn = get_db()
    posts = conn.execute('SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()

    return render_template('dashboard.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()

    if post:
        return render_template('post.html', post=post)
    else:
        flash('Post not found', 'danger')
        return redirect(url_for('index'))


@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        flash('Post updated successfully', 'success')
        return redirect(url_for('dashboard'))

    conn.close()

    if post and post[4] == session['user_id']:
        return render_template('edit_post.html', post=post)
    else:
        flash('You can only edit your own posts', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/post/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if post and post[4] == session['user_id']:
        conn.execute('DELETE FROM posts WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Post deleted successfully', 'success')
    else:
        flash('You can only delete your own posts', 'danger')
        conn.close()

    return redirect(url_for('dashboard'))


@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db()
        conn.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)', (title, content, session['user_id']))
        conn.commit()
        conn.close()
        flash('Post added successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)