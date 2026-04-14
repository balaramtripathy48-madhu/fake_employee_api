from flask import Flask, request, jsonify
from db_connect import get_connection

app = Flask(__name__)

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        'INSERT INTO employees(name, department, salary) VALUES(%s,%s,%s)',
        (data['name'], data['department'], data['salary'])
    )
    conn.commit()
    emp_id = cur.lastrowid
    cur.close(); conn.close()
    return jsonify({'message': 'Employee created', 'emp_id': emp_id}), 201

@app.route('/employees', methods=['GET'])
def get_all():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM employees')
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows)

@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_one(emp_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM employees WHERE emp_id=%s', (emp_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if row:
        return jsonify(row)
    return jsonify({'message': 'Not found'}), 404

@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()

    fields = []
    values = []

    if "name" in data:
        fields.append("name=%s")
        values.append(data["name"])

    if "department" in data:
        fields.append("department=%s")
        values.append(data["department"])

    if "salary" in data:
        fields.append("salary=%s")
        values.append(data["salary"])

    values.append(emp_id)

    query = f"UPDATE employees SET {', '.join(fields)} WHERE emp_id=%s"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": "Employee updated"}, 200

@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM employees WHERE emp_id=%s', (emp_id,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({'message': 'Employee deleted'})

if __name__ == '__main__':
    app.run(debug=True)