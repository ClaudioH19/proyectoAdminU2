from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM conversion_rates')
    data = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)