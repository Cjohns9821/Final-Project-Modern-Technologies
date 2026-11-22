from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "tickets.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, priority,
               assigned_to, status
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>IT Ticket Management System</title>
        <style>
            body {
                font-family: Arial;
                margin: 40px;
                background-color: #f4f4f4;
            }

            .ticket {
                background: white;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                box-shadow: 0px 0px 5px lightgray;
            }

            input, textarea, select {
                width: 300px;
                padding: 8px;
                margin-bottom: 10px;
            }

            button {
                padding: 10px 15px;
                background: #0078d4;
                color: white;
                border: none;
                cursor: pointer;
            }

            a {
                margin-right: 15px;
            }
        </style>
    </head>
    <body>

    <h1>IT Ticket Management System MVP</h1>

    <p>
        Track, assign, and manage IT support tickets.
    </p>

    <h2>Create Ticket</h2>

    <form action="/create" method="POST">

        <input type="text"
               name="title"
               placeholder="Ticket Title"
               required>

        <br>

        <textarea
            name="description"
            placeholder="Describe the issue"
            required></textarea>

        <br>

        <select name="priority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select>

        <br>

        <input type="text"
               name="assigned_to"
               placeholder="Assigned Technician"
               required>

        <br>

        <button type="submit">
            Create Ticket
        </button>

    </form>

    <hr>

    <h2>Current Tickets</h2>
    """

    for ticket in tickets:
        html += f"""
        <div class="ticket">

            <h3>{ticket[1]}</h3>

            <p>
                <strong>Description:</strong>
                {ticket[2]}
            </p>

            <p>
                <strong>Priority:</strong>
                {ticket[3]}
            </p>

            <p>
                <strong>Assigned To:</strong>
                {ticket[4]}
            </p>

            <p>
                <strong>Status:</strong>
                {ticket[5]}
            </p>

            <a href="/progress/{ticket[0]}">
                Mark In Progress
            </a>

            <a href="/close/{ticket[0]}">
                Close Ticket
            </a>

        </div>
        """

    html += """
    </body>
    </html>
    """

    return html


@app.route("/create", methods=["POST"])
def create_ticket():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    assigned_to = request.form["assigned_to"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (title, description, priority, assigned_to)
        VALUES (?, ?, ?, ?)
    """, (title, description, priority, assigned_to))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/progress/<int:ticket_id>")
def progress_ticket(ticket_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status='In Progress'
        WHERE id=?
    """, (ticket_id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/close/<int:ticket_id>")
def close_ticket(ticket_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status='Closed'
        WHERE id=?
    """, (ticket_id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
