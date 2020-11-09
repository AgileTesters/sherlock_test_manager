from flask import Blueprint, request, jsonify, abort, make_response

from sherlock_back.api import auth
from sherlock_back.api.controllers.scenarios import find_scenario, edit_test_scenario
from sherlock_back.api.controllers.shared.cycle_scenarios import create_test_scenario
from sherlock_back.api.controllers.shared.scenarios import mount_scenario_with_test_cases, scenarios_by_project, \
    change_status
from sherlock_back.api.controllers.tags import create_scenario_tag, delete_scenario_tag
from sherlock_back.api.data.model import StateType
from sherlock_back.api.helpers.string_operations import safe_fetch_content

scenarios = Blueprint('scenarios', __name__)


def default_check_for_scenario_resource(scenario_id):
    scenario = find_scenario(scenario_id)
    if scenario is None:
        abort(make_response(jsonify(message='SCENARIO_NOT_FOUND'), 404))
    elif scenario.state_code == StateType.removed:
        abort(make_response(jsonify(message='SCENARIO_NOT_FOUND'), 404))


@scenarios.route('/scenario/<int:scenario_id>', methods=['GET'])
@auth.login_required
def scenario_details(scenario_id):
    """Return Testcase Info."""
    scenario = find_scenario(scenario_id)
    default_check_for_scenario_resource(scenario_id)
    return make_response(jsonify(scenario))


@scenarios.route('/scenario/<int:scenario_id>/register_tag', methods=['POST'])
@auth.login_required
def register_tag(scenario_id):
    """POST endpoint for adding a tag to a scenario.

    Param:
        { tag': String - required }
    """
    default_check_for_scenario_resource(scenario_id)
    tag = safe_fetch_content(request, 'tag')
    create_scenario_tag(scenario_id, tag)
    return make_response(jsonify(message='TAG_CREATED'))


@scenarios.route('/scenario/<int:scenario_id>/remove_tag/<int:tag_id>', methods=['DELETE'])
@auth.login_required
def remove_tag(scenario_id, tag_id):
    default_check_for_scenario_resource(scenario_id)
    delete_scenario_tag(tag_id)
    return make_response(jsonify(message='TAG_REMOVED'))


@scenarios.route('/scenario/<int:scenario_id>/cases', methods=['GET'])
@auth.login_required
def get_scenario_n_tst_cases(scenario_id):
    """Return Scenario and Cases."""
    default_check_for_scenario_resource(scenario_id)
    scenario_with_cases = mount_scenario_with_test_cases(scenario_id)
    return make_response(jsonify(scenario_with_cases))


@scenarios.route('/project_scenarios/<int:project_id>', methods=['GET'])
@auth.login_required
def get_scenarios_by_project(project_id):
    """Return Scenarios + Tags."""
    scenarios_with_tags = scenarios_by_project(project_id)
    return make_response(jsonify(scenarios_with_tags))


@scenarios.route('/scenario/<int:scenario_id>/change_status/<string:action>', methods=['POST'])
@auth.login_required
def change_status_enable(scenario_id, action):
    if action.upper() not in ['DISABLE', 'ACTIVE', 'REMOVE']:
        return make_response(jsonify(message='ACTION_UNKNOWN'))
    change_status(scenario_id=scenario_id, action=action.upper())
    return make_response(jsonify(message='DONE'))


@scenarios.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenario.

    Params:
         {
            scenario_name: required,
            project_id: required,
         }
    """
    scenario_name = safe_fetch_content(request, 'scenario_name')
    project_id = safe_fetch_content(request, 'project_id')
    create_test_scenario(scenario_text=scenario_name, project_id=project_id)
    return make_response(jsonify(message='SCENARIO_CREATED'))


@scenarios.route('/scenario/<int:scenario_id>/edit', methods=['POST'])
@auth.login_required
def edit(scenario_id):
    """POST endpoint for editing existing scenarios.

    Param:
         {
           "scenario_text": required
         }
    """
    scenario_text = safe_fetch_content(request, 'scenario_text')
    default_check_for_scenario_resource(scenario_id)
    edit_test_scenario(scenario_id, scenario_text)
    return make_response(jsonify(message='SCENARIO_EDITED'))
