from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3
from settings import key
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = key.gen()

def opendb():
    global db, cursor
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()

def closedb():
    cursor.close()
    db.close()

@app.route("/")
def index():
    if 'isLogged' not in session:
        return redirect('login')
    elif 'isLogged' in session:
        return redirect('home')

@app.route("/home")
def home():
    opendb()
    query = 'select * from posts'
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('index.html', result=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    # ! Если со страницы приходит запрос
    if request.method == "POST":
        # ! получаем данные из полей
        login = request.form.get('login')
        password = request.form.get('password')
        opendb()
        query_info = 'select * from users where login=(?) and password=(?)'
        cursor.execute(query_info, [login, password])
        # ! создадим объект пользователя
        user = cursor.fetchone()
        if user is not None:
            session['isLogged'] = user[0]
            closedb()
            return redirect('/home')
        else:
            return '<h1>Неверный логин или пароль</h1>'
    # ! Если страница просто открывается
    else:
        return render_template('login.html')

@app.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    if request.method == "POST":
        title = request.form.get('title')
        descr = request.form.get('descr')
        date = str(datetime.datetime.today().replace(microsecond=0))
        opendb()
        cursor.execute('insert into posts(id, title, desrc, date) values(?,?,?,?)', [session['isLogged'],title, descr, date])
        db.commit()
        closedb()
        return redirect('/home')
    else:
        opendb()
        cursor.execute('select * from posts where id=(?)', [session['isLogged']])
        posts = cursor.fetchall()
        cursor.execute('select * from users_info where id=(?)', [session['isLogged']])
        user = cursor.fetchone()
        closedb()
    return render_template('cabinet.html', posts=posts, user=user)

if __name__ == "__main__":
    app.run(debug=True)