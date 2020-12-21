from flask import Blueprint, request, jsonify, make_response, abort

from sherlock_back.api import auth
from sherlock_back.api.controllers.cases import (find_test_case, change_status_to_active,
                                                 change_status_to_disable, change_status_to_removed,
                                                 edit_test_case, all_non_removed_cases_by_project)
from sherlock_back.api.controllers.shared.cases import (create_test_case,
                                                        self_parent_and_mismatch_check,
                                                        add_parent_id_to_cases, remove_parent_id_from_cases)
from sherlock_back.api.controllers.tags import create_case_tag, delete_case_tag
from sherlock_back.api.data.model import StateType
from sherlock_back.api.helpers.string_operations import safe_fetch_content

test_cases = Blueprint('test_cases', __name__)


@test_cases.route('/attach', methods=['POST'])
@auth.login_required
def attach_cases():
    project_id = safe_fetch_content(request, 'project_id')
    cases_array = safe_fetch_content(request, 'cases_array')
    parent_id = safe_fetch_content(request, 'parent_id')

    msg = self_parent_and_mismatch_check(project_id, cases_array, parent_id)
    if msg is None:
        add_parent_id_to_cases(
            cases_array=cases_array,
            project_id=project_id,
            target_case=parent_id
        )
        msg = "CASES_ATTACHED"
    return make_response(jsonify(msg))


@test_cases.route('/detach_cases', methods=['POST'])
@auth.login_required
def detach_cases():
    project_id = safe_fetch_content(request, 'project_id')
    cases_array = safe_fetch_content(request, 'cases_array')

    remove_parent_id_from_cases(
        cases_array=cases_array,
        project_id=project_id,
    )
    return make_response(jsonify("CASES_DETACHED"))


@test_cases.route('/find_by_project/<int:project_id>', methods=['GET'])
@auth.login_required
def fetch_test_cases(project_id):
    cases = all_non_removed_cases_by_project(project_id)
    return make_response(jsonify(cases))


@test_cases.route('/case/<int:test_case_id>', methods=['GET'])
@auth.login_required
def fetch_test_case_detail(test_case_id):
    test_case = find_test_case(test_case_id)
    if not test_case or test_case.state_code == StateType.removed:
        abort(make_response(jsonify(message='CASE_NOT_FOUND'), 404))
    return make_response(jsonify(test_case))


@test_cases.route('/case/<int:case_id>/register_tag', methods=['POST'])
@auth.login_required
def register_tag(case_id):
    """POST endpoint for adding a tag to a case.

    Param:
        {
        'tag': required
        }
    """
    tag = safe_fetch_content(request, 'tag')

    if find_test_case(test_case_id=case_id):
        create_case_tag(case_id=case_id, tag=tag)
        return make_response(jsonify(message='TAG_CREATED'))
    else:
        return make_response(jsonify(message='CASE_NOT_FOUND'), 404)


@test_cases.route('/case/<int:case_id>/remove_tag/<int:tag_id>', methods=['POST'])
@auth.login_required
def remove_tag(case_id, tag_id):
    if find_test_case(case_id):
        delete_case_tag(tag_id)
    return make_response(jsonify(message='TAG_REMOVED'))


@test_cases.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenarios.

    Param:
        {
         'test_case_text': required,
         'parent_id': required (0 for no parent),
         'project_id': required,
        }
    """

    test_case_text = safe_fetch_content(request, 'test_case_text')
    parent_id = safe_fetch_content(request, 'parent_id')
    project_id = safe_fetch_content(request, 'project_id')
    create_test_case(
        test_case_text = test_case_text,
        parent_id=parent_id,
        project_id=project_id,
    )
    return make_response(jsonify(message='CASE_CREATED'))


@test_cases.route('/case/<int:case_id>/change_status/active', methods=['POST'])
@auth.login_required
def test_case_change_status_to_active(case_id):
    change_status_to_active(case_id)
    return make_response(jsonify(message='DONE'))


@test_cases.route('/case/<int:case_id>/change_status/disable', methods=['POST'])
@auth.login_required
def test_case_change_status_to_disable(case_id):
    change_status_to_disable(case_id)
    return make_response(jsonify(message='DONE'))


@test_cases.route('/case/<int:case_id>/change_status/remove', methods=['POST'])
@auth.login_required
def test_case_change_status_to_remove(case_id):
    change_status_to_removed(case_id)
    return make_response(jsonify(message='DONE'))


@test_cases.route('/case/<int:case_id>/edit', methods=['POST'])
@auth.login_required
def edit_case(case_id):
    """POST endpoint for edit scenarios.

    Param:
        {
            'test_case_text': required,
        }
    """
    test_case_text = safe_fetch_content(request, 'test_case_text')
    edit_test_case(case_id, test_case_text)
    return make_response(jsonify(message='CASE_EDITED'))
