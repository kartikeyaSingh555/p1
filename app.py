from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "university_secret_key"
DATABASE = "database.db"

def get_db():
    return sqlite3.connect(DATABASE)

@app.route('/')
def index():
    return redirect('/login')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        reg_no = request.form['reg_no']
        password = request.form['password']
        role = request.form['role']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO User (username, reg_no, password, role) VALUES (?,?,?,?)",
            (username, reg_no, password, role)
        )
        conn.commit()
        conn.close()
        return redirect('/login')

    return render_template('signup.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM User WHERE reg_no=? AND password=?",
            (reg_no, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            return redirect('/home')

    return render_template('login.html')

# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('home.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- ADD EVENT (ADMIN) ----------------
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if session.get('role') != 'Admin':
        return redirect('/home')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Event (title, description, event_date) VALUES (?,?,?)",
            (title, description, event_date)
        )
        conn.commit()
        conn.close()
        return redirect('/events')

    return render_template('add_event.html')

# ---------------- VIEW EVENTS ----------------
@app.route('/events')
def events():
    if 'username' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Event ORDER BY event_date DESC")
    events = cur.fetchall()
    conn.close()

    return render_template('events.html', events=events)

# ---------------- VIEW BLOGS ----------------
@app.route('/blogs/<int:event_id>')
def blogs(event_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Event WHERE event_id=?", (event_id,))
    event = cur.fetchone()

    cur.execute("SELECT * FROM Blog WHERE event_id=?", (event_id,))
    blogs = cur.fetchall()

    conn.close()
    return render_template('blogs.html', event=event, blogs=blogs)

# ---------------- ADD BLOG (ADMIN) ----------------
@app.route('/add_blog/<int:event_id>', methods=['GET', 'POST'])
def add_blog(event_id):
    if session.get('role') != 'Admin':
        return redirect('/home')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Blog (event_id, title, content, created_at) VALUES (?,?,?,datetime('now'))",
            (event_id, title, content)
        )
        conn.commit()
        conn.close()
        return redirect(f'/blogs/{event_id}')

    return render_template('add_blog.html')

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
