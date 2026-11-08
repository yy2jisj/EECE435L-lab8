from contextlib import closing

from flask import jsonify

from app import app, connect_to_db, create_db_table


@app.get("/get_users")
def get_user_names():
    with closing(connect_to_db()) as conn:
        rows = conn.execute("SELECT name FROM users ORDER BY user_id").fetchall()
    return jsonify([name for (name,) in rows])


if __name__ == "__main__":
    create_db_table()
    app.run(host="0.0.0.0", port=3000)
