import random
import string

from flask import Flask
from flask import request, abort, send_from_directory, make_response
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

quests = {
    1: {"key": "156", "hint": "Первая цифра - 1", "next_page": "task2.html"},
    2: {"key": "маракуйя", "next_page": "task3.html"},
    3: {"key": "ede", "next_page": "final.html"}
}

quests_try = {
    1: {"user_s0fus_id": 0, "user_val_id": 4},
    2: {},
    3: {}
}


@app.route('/')
def render_main():
    return send_from_directory(".", "index.html")


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory('.', filename)


@app.route('/<int:quest_id>/')
def verify(quest_id):
    username = request.cookies.get('username')
    resp = make_response()

    if username is None:
        username = "".join([random.choice(string.ascii_letters) for _ in range(32)])
        resp.set_cookie('username', username)

    quest_try = quests_try[quest_id]
    if username not in quest_try:
        quest_try[username] = 0

    presented_key = request.args.get('key') or ''
    presented_key = presented_key.lower()

    if quest_id not in quests:
        abort(404, description="Resource not found")

    print(f"log: Q {quest_id} TRY {quest_try[username]} by {username}")

    quest = quests[quest_id]
    # correct answer
    if presented_key == quest["key"]:
        resp.set_data(quest["next_page"])
        return resp

    # wrong answer
    if "hint" in quest and quest_try[username] >= 5:
        resp.set_data(quest["hint"])
    else:
        quest_try[username] = quest_try[username] + 1
        resp.set_data("Неверный ответ")
    return resp, 400


@app.route('/reset/')
def reset_try():
    for quest_id in quests_try:
        print(f"log: Q {quest_id} WAS {quest_try} --> 0")
        quest_try = 0
    return "Success"


if __name__ == '__main__':
    app.run()
