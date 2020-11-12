"""Sherlock User Controllers and Routes."""
from flask import Blueprint, jsonify, make_response

from sherlock_back.api import auth
from sherlock_back.api.controllers.cycles import last_cycle
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats
from sherlock_back.api.data.model import Project, ProjectSchema
from sherlock_back.api.data.model import CycleCases

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/', methods=['GET'])
@auth.login_required
def home():
    schema = ProjectSchema(many=True)
    projects = schema.dump(Project.query.all()).data

    for item in projects:
        project_last_cycle = last_cycle(item['id'])

        item['have_cycle'] = False
        if project_last_cycle:
            item['have_cycle'] = True
            cycle_cases_h = CycleCases.query.filter_by(
                cycle_id=project_last_cycle.id).all()

            item['current_cycle'] = project_last_cycle.cycle
            item['cycle_state'] = project_last_cycle.state_code.value
            item['stats'] =  count_cycle_stats(cycle_cases_h)
        else:
            item['cycle_state'] = "nocycle"
    return make_response(jsonify(projects_qtd=len(projects),projects=projects))