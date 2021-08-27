import random
import string

from flask import Flask
from flask import request, abort, send_from_directory, make_response
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

quests = {
    1: {"key": "феерия", "hint": "Кто много знает — много и ошибается", "next_page": "tv.html"},
    2: {"key": "преступники", "hint": "То, как я его называю", "next_page": "catfood.html"},
    3: {"key": "оладушки", "hint": "Ласковое название", "next_page": "greekgod.html"},
    4: {"key": "нарцисс", "next_page": "book.html"},
    5: {"key": "лермонтов", "hint": "Год прошёл!" ,"next_page": "pants.html"},
    6: {"key": "letitsnow", "hint": "По-английски", "next_page": "whoreshirt.html"},
    7: {"key": "5", "next_page": "next.html"},
    8: {"key": "156", "next_page": "codetrees.html"},
    9: {"key": "квиндт", "hint": "По-русски", "next_page": "almostthere.html"}
}

quests_try = {
    1: {"user_s0fus_id": 0, "user_val_id": 4},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
    8: {},
    9: {}

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
        username = "mock_username"
        # # TODO: send cookies in js
        # username = "".join([random.choice(string.ascii_letters) for _ in range(32)])
        # resp.set_cookie('username', username)

    quest_try = quests_try[quest_id]
    if username not in quest_try:
        quest_try[username] = 0

    presented_key = request.args.get('key') or ''
    presented_key = presented_key.lower()
    presented_key = presented_key.replace(" ", "")

    if quest_id not in quests:
        abort(404, description="Resource not found")

    quest = quests[quest_id]
    print(f"log: Q {quest_id} TRY {quest_try[username]} by {username}")
    print(f"log: Q {quest_id} IN {quest['key']} WANT {presented_key}")

    # correct answer
    if presented_key == quest["key"]:
        resp.set_data(quest["next_page"])
        return resp

    # wrong answer
    if "hint" in quest and quest_try[username] >= 4:
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
