from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    conn.close()

    html = """
    <h1>IT Ticket Management System</h1>

    <form method="POST" action="/create">
        <input name="title" placeholder="Ticket Title" required><br><br>

        <textarea name="description"
                  placeholder="Description"
                  required></textarea><br><br>

        <button type="submit">Create Ticket</button>
    </form>

    <hr>
    """

    for ticket in tickets:
        html += f"""
        <h3>{ticket[1]}</h3>
        <p>{ticket[2]}</p>
        <p>Status: {ticket[3]}</p>
        <a href="/close/{ticket[0]}">Close Ticket</a>
        <hr>
        """

    return html


@app.route("/create", methods=["POST"])
def create_ticket():
    title = request.form["title"]
    description = request.form["description"]

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tickets (title, description) VALUES (?, ?)",
        (title, description)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/close/<int:id>")
def close_ticket(id):
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tickets SET status='Closed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
