# Web-приложение
# Flask - минимализм с возможностью расширения
# устанавливаем pip install flask
# Django - всё включено (не используем)
from idlelib.macosx import setupApp
from importlib.metadata import requires
from wsgiref.util import request_uri

from flask import Flask, url_for, request, render_template
import sqlite3

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


@app.route('/countdown')  # Декоратор
def cdown():
    lst = [str(x) for x in reversed(range(11))]
    lst.append('Поехали!')
    return '<br>'.join(lst)


@app.route('/about')  # Декоратор
def about():
    return """
    Это страница с более подробной информацией.
    <br>А вот <a href="/genres">тут</a> про жанры.
    <br>А вот <a href="/countdown">тут</a> обратный отсчёт
    <br>А вот <a href="/flag">тут</a> Флаг.
    <br><a href="/home">назад></a>
    """


@app.route('/genres')
def genres():
    temp = []
    con = sqlite3.connect('db/books_bd.sqlite')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM genres").fetchall()
    cur.close()
    con.close()
    for _, name in res:
        temp.append(name)
    temp = list(map(lambda x: '<li>' + x + '</li>', temp))
    res = '<br>'.join(temp)
    result = f"""
    <!DOCTYPE html>
<html lang="ru">
<head>
    <!--как будет отображаться на странице-->
    <meta charset="UTF-8">
    <link rel="stylesheet" href="{url_for("static", filename='css/styles.css')}">
    <title>Жанры</title>
</head>
<body>
<!--что будут отображаться на странице-->
<h1>А вот и жанры:</h1>
<ol>
{res}
<ol>
</body>
</html>
    """
    return result


@app.route('/flag')
def flag():
    return f"""<img src="{url_for("static", filename='images/flag.webp')}" 
    height="40" width="60"
    alt=\"Нету флага\">"""


# <name> - строка
# <num:int> - целое
# <num:float> - десятичная дробь

@app.route("/greet", defaults={'name': None})
@app.route("/greet/<name>")
def greeting(name):
    if name is None:
        return '<h1> Не с кем здороваться!!!</h1>'
    return f"""
    <!DOCTYPE html>
<html lang="ru">
<head>
    <!--как будет отображаться на странице-->
    <meta charset="UTF-8">
    <meta name="description" content="Описание страницы сайта.">
    <link rel="stylesheet" href="{url_for('static', filename='css/styles.css')}">
    <title>Приветствуем тебя, {name} </title>
</head>
<body>
<h1>{name.capitalize()}, мы приветствуем тебя</h1>
<!--что будут отображаться на странице-->
<h1>А вот и жанры:</h1>
{name}
</body>
</html>
    """


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
