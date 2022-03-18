import json
import random
import math

import numpy as np

import connexion
from pplabel.config import db
from .base import crud
from ..model import Task, Project
from ..schema import TaskSchema
from . import project
from pplabel.api.util import abort

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)


def get_by_project(project_id):
    if connexion.request.method == "HEAD":
        return get_stat_by_project(project_id)
    Project._exists(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    return TaskSchema(many=True).dump(tasks), 200


# TODO: dont lazy load annotations in tasks
def get_stat_by_project(project_id):
    Project._exists(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    ann_count = 0
    for task in tasks:
        if len(task.annotations) != 0:
            ann_count += 1
    res = {"finished": ann_count, "total": len(tasks)}
    return res, 200, res
