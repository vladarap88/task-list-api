from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
from .route_utilities import validate_model


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError as e:
        if e.args[0] == "title" or e.args[0] == "description":
            response = {"details": "Invalid data"}
        return make_response(response, 400)

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.create_response()}

    return response, 201


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Task.title == title_param)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.ilike(f"%{completed_at_param}%"))

    query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = [task.create_response() for task in tasks]
    return tasks_response


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    response = {"task": task.create_response()}

    return response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {"task": task.create_response()}

    return response


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}

    return response
