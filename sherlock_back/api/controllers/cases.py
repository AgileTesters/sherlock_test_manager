from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import find_cycle_case
from sherlock_back.api.data.model import (Case, TestCaseSchema, StateType)


def all_non_removed_cases_by_project(project_id):
    schema = TestCaseSchema(many=True)
    cases_query_result = Case.query.filter_by(
        project_id=project_id).filter_by(parent_id=0).filter(
        Case.state_code != StateType.removed).all()
    cases_to_be_grouped_query_result = Case.query.filter_by(
        project_id=project_id).filter(
        Case.state_code != StateType.removed).filter(Case.project_id > 0).all()

    main_cases = schema.dump(cases_query_result)
    main_cases = sorted(main_cases, key=lambda k: k['order_index'])

    for index, case in enumerate(main_cases):
        case['child_cases'] = []
        case['exhibition_order'] = index

    to_be_grouped_cases = schema.dump(cases_to_be_grouped_query_result)
    to_be_grouped_cases = sorted(to_be_grouped_cases, key=lambda k: k['order_index'])

    for case in to_be_grouped_cases:
        for main_case in main_cases:
            if case['parent_id'] == main_case['id']:
                # snapshot of the size of child_cases
                case['exhibition_order'] = len(main_case.get('child_cases', 0)) + 1
                main_case['child_cases'].append(case)
    return main_cases


# def active_cases_by_project(project_id):
#     schema = TestCaseSchema(many=True)
#     cases_query_result =  Case.query.join(
#         Scenario, Case.scenario_id == Scenario.id).filter(
#         Scenario.project_id == project_id).filter(
#         Case.state_code == StateType.active).all()
#     return schema.dump(cases_query_result).data


def find_test_case(test_case_id):
    """Return Testcase Info."""
    test_case = Case.query.filter_by(id=test_case_id).first()
    tst_case_schema = TestCaseSchema(many=False)
    return tst_case_schema.dump(test_case)


def change_status_to_disable(case_id):
    __change_test_case_state_code(
        case_id=case_id,
        state=StateType.disable
    )
    __change_cycle_test_case_state_code(
        case_id=case_id,
        state_code=StateType.blocked
    )


def change_status_to_active(case_id):
    __change_test_case_state_code(
        case_id=case_id,
        state=StateType.active
    )
    __change_cycle_test_case_state_code(
        case_id=case_id,
        state_code=StateType.active
    )


def change_status_to_removed(case_id):
    __change_test_case_state_code(
        case_id=case_id,
        state=StateType.removed
    )
    __change_cycle_test_case_state_code(
        case_id=case_id,
        state_code=StateType.removed
    )


def __change_test_case_state_code(case_id, state):
    test_case = find_test_case(case_id)
    test_case.state_code = state
    db.session.add(test_case)
    db.session.commit()


def __change_cycle_test_case_state_code(case_id, state_code):
    """
        Change the state code of the CYCLE test case
    """
    # JUST TO FIND THE PROJECT_ID
    case = find_test_case(test_case_id=case_id)

    cycle = last_cycle(case.project_id)
    cycle_case = find_cycle_case(cycle_id=cycle.id, case_id=case_id)
    if cycle and cycle_case and state_code:
        cycle_case.state_code = state_code
        db.session.add(cycle_case)
        db.session.commit()


def edit_test_case(case_id, text_case_string):
    case = find_test_case(case_id)
    case.name = text_case_string
    db.session.add(case)
    db.session.commit()
