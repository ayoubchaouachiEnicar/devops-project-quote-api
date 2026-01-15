from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory storage
todos = []
next_id = 1

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    return jsonify(todo)

@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing title")
    global next_id
    todo = {
        'id': next_id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'completed': False,
        'created_at': datetime.utcnow().isoformat()
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    if not request.json:
        abort(400, description="Invalid data")
    todo['title'] = request.json.get('title', todo['title'])
    todo['description'] = request.json.get('description', todo['description'])
    todo['completed'] = request.json.get('completed', todo['completed'])
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)