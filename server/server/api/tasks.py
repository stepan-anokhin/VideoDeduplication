from http import HTTPStatus

from flask import jsonify, request, abort

from server.queue.instance import queue, request_transformer
from server.queue.model import Task, TaskStatus
from .blueprint import api
from .helpers import parse_enum_seq, parse_positive_int


@api.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = queue.get_task(task_id)
    if task is None:
        abort(HTTPStatus.NOT_FOUND.value, f"Task id not found: {task_id}")
    return jsonify(task.asdict())


@api.route("/tasks/", methods=["GET"])
def list_tasks():
    status = parse_enum_seq(request.args, "status", {status.value for status in TaskStatus})
    offset = parse_positive_int(request.args, "offset", 0)
    limit = parse_positive_int(request.args, "limit", 100)
    tasks, total = queue.list_tasks(status=status, limit=limit, offset=offset)
    return jsonify({"items": list(map(Task.asdict, tasks)), "total": total})


@api.route("/tasks/", methods=["POST"])
def post_task():
    request_payload = request.get_json()
    if request_payload is None:
        abort(HTTPStatus.BAD_REQUEST.value, f"Expected valid 'application/json' payload.")

    task_request = None
    try:
        task_request = request_transformer.fromdict(request_payload)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST.value, f"Invalid request.")

    task = queue.dispatch(task_request)
    return jsonify(task.asdict())


@api.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if not queue.exists(task_id):
        abort(HTTPStatus.NOT_FOUND.value, f"Task id not found: {task_id}")
    queue.delete(task_id)
    return "", HTTPStatus.NO_CONTENT.value


@api.route("/tasks/<task_id>", methods=["PATCH"])
def cancel_task(task_id):
    if not queue.exists(task_id):
        abort(HTTPStatus.NOT_FOUND.value, f"Task id not found: {task_id}")

    request_payload = request.get_json()
    if request_payload is None:
        abort(HTTPStatus.BAD_REQUEST.value, f"Expected valid 'application/json' payload.")

    if request_payload != {"status": TaskStatus.REVOKED.value}:
        abort(HTTPStatus.BAD_REQUEST.value, f"Invalid request.")

    queue.terminate(task_id)
    return "", HTTPStatus.NO_CONTENT.value
