"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, make_response, abort

from sherlock_back.api import auth
from sherlock_back.api.controllers.cycles import (cycle_timeline_resume_by_project,
                                                  get_cycle_case_stats, close_cycle, last_cycle,
                                                  change_cycle_case_state_code)
from sherlock_back.api.controllers.projects import find_project
from sherlock_back.api.controllers.shared.cycle_case import parse_test_cases_for_cycle
from sherlock_back.api.controllers.shared.cycles import create_cycle
from sherlock_back.api.data.model import StateType

from sherlock_back.api.helpers.string_operations import safe_fetch_content

cycles = Blueprint('cycle', __name__)


@cycles.route('/project/<int:project_id>/timeline/<int:cycle_limit>', methods=['GET'])
@cycles.route('/project/<int:project_id>/timeline', methods=['GET'])
@auth.login_required
def get_cycle_timeline_resume(project_id, cycle_limit=7):
    cycle_parsed = cycle_timeline_resume_by_project(project_id=project_id, cycle_limit=cycle_limit)
    return make_response(jsonify(cycle_parsed))


@cycles.route('/cycle/<int:cycle_id>/resume', methods=['GET'])
@auth.login_required
def get_cycle_resume_(cycle_id):
    return make_response(jsonify(get_cycle_case_stats(cycle_id)))


@cycles.route('/cycle/<int:cycle_id>/close', methods=['POST'])
@auth.login_required
def close(cycle_id):
    # TODO: Check untested cases.
    """POST endpoint for closing cycles.
    Param:
        {
            reason: required,
        }
    """
    reason = safe_fetch_content(request, 'reason')
    close_cycle(cycle_id, reason, g.user.id)

    return make_response(jsonify(message='CYCLE_CLOSED'))


@cycles.route('/cycle', methods=['POST'])
@auth.login_required
def create():
    """POST endpoint for new cycles.
    Param:
        {
            'cycle_name': required but can be empty
            'project_id':  required
        }
    """
    project_id = safe_fetch_content(request, 'project_id')

    project = find_project(project_id)
    if not project:
        return make_response(jsonify(message='PROJECT_NOT_FOUND'), 404)

    project_last_cycle = last_cycle(project_id)

    if project_last_cycle and project_last_cycle.state_code == StateType.active:
        return make_response(jsonify(message='CURRENT_CYCLE_ACTIVE'))

    cycle_id = create_cycle(
        project_id=project_id,
        cycle_name=request.json.get('cycle_name', None)
    )

    if not cycle_id:
        return make_response(jsonify(message='CYCLE_NOT_CREATED'), 400)
    else:
        return make_response(jsonify(message='CYCLE_CREATED', cycle_id=cycle_id))


@cycles.route('/cycle/<int:cycle_id>/project/<int:project_id>/cases', methods=['GET'])
@auth.login_required
def get_cases_for_cycle(project_id, cycle_id):
    scenario_with_cases = parse_test_cases_for_cycle(cycle_id, project_id)
    return make_response(jsonify(scenario_with_cases))


# @cycles.route('/cycle/<int:cycle_id>/project/<int:project_id>/cases/case/<int:case_id>',methods=['GET'])
# @auth.login_required
# def change_cycle_case_state_code_(project_id, cycle_id, case_id):
#     """ Endpoint for changing the cycle cases state_code .
#     Param:
#         {
#             'action': required
#         }
#     """
#     action = safe_fetch_content(request, 'action')
#     project_last_cycle = last_cycle(project_id)
#
#     if cycle_id != project_last_cycle.id:
#         return make_response(jsonify(message='NOT_LAST_CYCLE'))
#
#     if action not in StateType.__members__:
#         return abort(make_response(jsonify(message='ACTION_UNKNOW'), 400))
#
#     changed = change_cycle_case_state_code(
#         action=action,
#         cycle_id=cycle_id,
#         case_id=case_id
#     )
#     if changed:
#         return make_response(jsonify(message='CYCLE_CASE_UPDATED'))
#     return abort(make_response(jsonify(message='CYCLE_CASE_NOT_UPDATED'), 400))
