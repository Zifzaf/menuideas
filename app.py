from flask import Flask, render_template
import sqlite3
import random

app = Flask(__name__)


@app.route("/")
def index():
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute("SELECT menu FROM menus")
    menu_items = cursor.fetchall()
    conn.close()
    random.shuffle(menu_items)

    return render_template("index.html", menu_items=menu_items)


if __name__ == "__main__":
    app.run(debug=True)
