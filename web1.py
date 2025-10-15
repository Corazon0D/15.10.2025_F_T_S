# Web-приложение
# Flask - минимализм с возможностью расширения
# устанавливаем pip install flask
# Django - всё включено (не используем)
from idlelib.macosx import setupApp
from importlib.metadata import requires
from wsgiref.util import request_uri

from flask import Flask, url_for, request
import sqlite3

app = Flask(__name__)


@app.route('/')  # Декоратор
@app.route('/home')
def index():
    return """
    Я Ваше первое приложение.
    <br>Подробнее <a href="/about">здесь></a>
    
    """


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
    <link rel="stylesheet" href="{url_for("static", filename='css/styles.css')}">
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
        return """
        <!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="../static/css/styles.css">
    <title>Форма регистрации</title>
</head>

<body>
    <h1>Форма регистрации</h1>
    <form class="login-form" method="post">
        <fieldset>
            <legend>Личные данные</legend>
            <label class="form-label" for="email">Ваш email:</label>
            <input class="form-control" name="email" id="email" placeholder="Введите E-mail" required>
            <label class="form-label" for="password">Пароль:</label>
            <input class="form-control" type="password" name="password" id="password" placeholder="Введите пароль" required>
        </fieldset>
        <div class="form-group">
            <label class="form-label" for="gender">Ваш пол</label>
            <select class="form-select" name="genderSelect" id="gender">
                <option>М</option>
                <option>Ж</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label" for="about">Немного о себе:</label>
            <textarea class="form-control" name="about" id="about" cols="30" rows="5"></textarea>
        </div>
        <br>
            <div class="form-check form-group">
            <input class="form-check-input" type="checkbox" name="remember" id="remember">
            <label class="form-label" for="remember">&nbsp;Запомни меня</label>
        </div>
        <div class="pos">
        <button class="btn btn-dark" type="submit">Зарегистрироваться</button>
        </div>
    </form>
</body>

</html>
        """
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        genderSelect = request.form.get('genderSelect')
        if genderSelect == 'М':
            status1 = 'Мужской'
        else:
            status1 = 'Женский'
        about = request.form.get('about')
        remember = request.form.get('remember')
        if remember == 'on':
            status = 'Запомнить'
        else:
            status = "Не запоминать"

        return f"""Ура форма отправлена с <b>E-mail</b>: {email}
        <br><b>Пароль был</b>: {password},
        <br><b>Пол</b>: {status1},
        <br><b>О себе написал</b>: {about},
        <br>Просил <b>{status}</b> его
        """


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
