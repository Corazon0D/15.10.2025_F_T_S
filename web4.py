# Web-приложение
# Flask - минимализм с возможностью расширения
# устанавливаем pip install flask
# Django - всё включено (не используем)
from idlelib.macosx import setupApp
from importlib.metadata import requires
from wsgiref.util import request_uri

from flask import Flask, url_for, request, render_template
import sqlite3

# Flask и Jinja РАБОТАЕМ
app = Flask(__name__)


@app.route('/')  # Декоратор
@app.route('/home')
def index():
    params = {
        'user': 'слушатель от ИПАП',
        'tutle': 'Пример рендеренга'
    }
    return render_template('index1.html', **params)


# return render_template('index1.html',
# user='слушатель от ИПАП'
# title='Пример рендеринга')

# ДЗ  Делаю обратный отсчёт ! ! !
@app.route('/countdown')  # Декоратор
def cdown():
    lst = [str(x) for x in reversed(range(11))]
    lst.append('Поехали!')
    return render_template('countdown.html', countdown=lst) #'<br>'.join(lst)


@app.route('/conditions-sample/<int:number>')
def event_odd(number):  # Чётное не чётное
    return render_template('event_odd.html',
                           number=number,
                           title='Чётное или не чётное')

# ДЗ ТУТА Я СДЕЛАЛ ! ! !
@app.route('/about')  # Декоратор
def about():
    return render_template('about.html')

# ДЗ с этого начал ! ! !
@app.route('/genres')
def genres():
    temp = []
    con = sqlite3.connect('db/books_bd.sqlite')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM genres").fetchall()
    genres = [row[1] for row in res]  # получаем только названия жанров
    cur.close()
    con.close()
    return render_template('genres.html', genres=genres)

# ДЗ ФЛАГ сделал ! ! !
@app.route('/flag')
def flag():
    return render_template('flag.html')


# <name> - строка
# <num:int> - целое
# <num:float> - десятичная дробь

# ТА-ТА-ТААА Я Заканчиваю  ! ! ! !
@app.route("/greet", defaults={'name': None})
@app.route("/greet/<name>")
def greeting(name):
    return render_template('greet.html', name=name, genres=genres)


@app.route('/form-sample', methods=['GET', 'POST'])
def form_sample():
    if request.method == 'GET':
        return render_template('form_sample.html',
                               form_title='Форма для регистрации')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        genderSelect = request.form.get('genderSelect')
        if genderSelect == 'М':  #
            status1 = 'Мужской'  #
        else:  #
            status1 = 'Женский'  #
        # или так
        # genderSelect ='Мужской' if genderSelect =='М' else 'Женский'
        about = request.form.get('about')
        remember = request.form.get('remember')
        if remember == 'on':
            status = 'Запомнить'
        else:
            status = "Не запоминать"

        return render_template('result.html',
                               title='Результат отправки',
                               email=email, password=password,
                               status1=genderSelect, about=about,
                               status=status)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
