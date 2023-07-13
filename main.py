# Написать web-сервер на Go/Python:
import sqlite3, os
from datetime import datetime
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

### 1.4 Добавить эндпойнт /metrics который в prometheus-совместимом 
### формате будет отдавать метрики по количеству обработанных GET и POST запросов
metrics = PrometheusMetrics(app)

### 1.1 При GET запросе на эндпойнт /hello сервер должен отдавать текст “Hello Page”
@app.route("/hello")
def hello_page():
    # Return response Hello page
    return "Hello Page"

# 1.2 При POST запросе на эндпойнт /user с параметром name=*имя пользователя* 
#   (пример: .../user name=Joe) сервер должен сохранять в текстовых лог-файл имя 
#   пользователя и время запроса (формат - name: hh:mm:ss - dd.mm.yyyy)
@app.route('/user', methods=["POST"])
def add_user():
    try:
        # Get username from request
        name = request.json['name']
        # Get time
        date = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
        
        # export log with user and date to file log.txt
        log = "Name: " + name + ", Time: " + str(date)
        with open('log.txt', 'a') as file:
            file.write(log + '\n')
        print(log)

        # If IMPORT_TO_DB is True then put user information to sqlite by calling definition of it
        import_to_db = os.environ.get("IMPORT_TO_DB")
        if import_to_db == "True":
            put_user(name, date)

        resp = '{"status": "success", "import_to_db": "'+ import_to_db +'"}'
        return resp
    except Exception as e:
        print(e)
        resp = '{"status": "failed", "message":"' + str(e) + '"}'
        return resp, 500


### 1.3 Добавить возможность опционально использования SQLite вместо файла 
###     лога для сохранения имени пользователя и времени в таблицу users и возвращать 
###     эти данные по GET запросу с теми же параметрами (пример: .../user?name=Joe)
def get_db_connection():
    # Connection to sqlite database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/user", methods=["GET"])
def get_user():
    # Geting username from request
    user = str(request.args.get('name'))

    # Con to database, and selecting user form db
    conn = get_db_connection()
    resp = conn.execute('SELECT * FROM users WHERE user = (?)',[user]).fetchone()
    conn.close()

    # If user not found, return not found resp with 404
    if resp is None:
        resp = '{"status": "User not found"}'
        return resp, 404

    # User was found retur json with user
    date = str(resp[3])
    resp = '{"status": "found", "data": [{"user":"'+ user +'","date":"'+ date +'"}]}'
    return resp

def put_user(user, date):
    # Inserting new user into database
    conn = get_db_connection()
    conn.execute("INSERT INTO users (user, date) VALUES (?, ?)",(user, date))
    conn.commit()
    conn.close()
    print("User " + user + " was inserted to DB.")


app.run()
