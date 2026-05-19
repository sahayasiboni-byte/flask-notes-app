from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def create_table():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_table()


@app.route("/")
def index():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title")
    content = request.form.get("content")

    if title != "" and content != "":
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO notes(title, content) VALUES (?, ?)",
            (title, content)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_note(id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
