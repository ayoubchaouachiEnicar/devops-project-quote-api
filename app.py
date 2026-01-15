from flask import Flask, jsonify, request, abort
from datetime import datetime, timezone
import uuid
import logging
import structlog
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, REGISTRY  # for custom + force expose
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

app = Flask(__name__)

# Structured logging (JSON)
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()

# Prometheus setup
metrics = PrometheusMetrics(app, group_by='url_rule')

# Custom counter (reliable way)
todos_created = Counter(
    'todos_created_total',
    'Total number of todos created',
    registry=metrics.registry  # share registry
)

# Force expose /metrics if not auto-registering (workaround for some setups)
@app.route('/metrics')
def metrics_endpoint():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

# Tracing setup
trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "todo-api"})))
jaeger_exporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))
FlaskInstrumentor().instrument_app(app)

# Request context for logs
@app.before_request
def add_request_context():
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    logger.info("Request started", method=request.method, path=request.path, ip=request.remote_addr)

@app.after_request
def log_completion(response):
    logger.info("Request completed", status=response.status_code)
    return response

# In-memory storage
todos = []
next_id = 1

@app.route('/todos', methods=['GET'])
def get_todos():
    logger.info("Fetching all todos", count=len(todos))
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo not found")
    logger.info("Fetched todo", todo_id=todo_id)
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
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    todos.append(todo)
    next_id += 1
    todos_created.inc()  # increment custom metric
    logger.info("Todo created", todo_id=todo['id'], title=todo['title'])
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
    logger.info("Todo updated", todo_id=todo_id)
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    logger.info("Todo deleted", todo_id=todo_id)
    return jsonify({'message': 'Todo deleted'})

@app.errorhandler(404)
def not_found(error):
    logger.error("Not found error", error=str(error))
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    logger.error("Bad request error", error=str(error))
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)