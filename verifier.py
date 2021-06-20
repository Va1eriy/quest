from flask import Flask
from flask import redirect, request, abort, send_from_directory
from flask_cors import CORS


app = Flask(__name__, template_folder='.')
CORS(app)


quests = {
    1: {"key": "156", "hint": "Первая цифра - 1","next_page": "task2.html"},
    2: {"key": "маракуйя", "next_page": "task3.html"},
    3: {"key": "ede", "next_page": "final.html"}
}

quests_try= {
    1: 0,
    2: 0,
    3: 0
}

@app.route('/')
def render_main():
    return send_from_directory(".", "index.html")


@app.route('/<path:filename>')
def send_file(filename):
      return send_from_directory('.', filename)


@app.route('/<int:quest_id>/')
def verify(quest_id):
    presented_key = request.args.get('key')
    presented_key = presented_key.lower()

    if quest_id not in quests:
        abort(404, description="Resource not found")

    quest = quests[quest_id]
    if presented_key == quest["key"]:
        return quest["next_page"]
        #return send_from_directory('.', quest["next_page"])
    else:
        print(f"log: Q {quest_id} TRY {quests_try[quest_id]}")
        if  "hint" in quest and quests_try[quest_id] >= 5:
            return quest["hint"], 400
        quests_try[quest_id] = quests_try[quest_id]+1
        return "Wrong key", 400

@app.route('/reset/')
def reset_try():
    for quest_id in quests_try:
        print(f"log: Q {quest_id} WAS {quests_try[quest_id]} --> 0")
        quests_try[quest_id] = 0
    return "Success"

if __name__ == '__main__':
    app.run()
