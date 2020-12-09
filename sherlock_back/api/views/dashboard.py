"""Sherlock User Controllers and Routes."""
from flask import Blueprint, jsonify, make_response

from sherlock_back.api import auth
from sherlock_back.api.controllers.cycles import last_cycle, cycle_cases_by_project
from sherlock_back.api.controllers.projects import get_all_projects
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats
from sherlock_back.api.data.model import CycleCases

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/', methods=['GET'])
@auth.login_required
def home():
    projects = get_all_projects()

    for item in projects:
        project_last_cycle = last_cycle(item['id'])
        if project_last_cycle:
            project_id = project_last_cycle.id
            item['have_cycle'] = True
            item['current_cycle'] = project_last_cycle.cycle
            item['cycle_state'] = project_last_cycle.state_code.value
        else:
            item['have_cycle'] = False
            project_id = None
        cycle_cases = cycle_cases_by_project(project_id)
        item['stats'] = count_cycle_stats(cycle_cases)

    return make_response(jsonify(projects_qtd=len(projects),projects=projects))