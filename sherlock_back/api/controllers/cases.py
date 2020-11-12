from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import find_cycle_case, last_cycle
from sherlock_back.api.data.model import (Case, TestCaseSchema, StateType, EntityType)


def all_non_removed_cases_by_project(project_id):
    schema = TestCaseSchema(many=True)
    cases_query_result = Case.query.filter_by(
        project_id=project_id).filter(
        Case.state_code != StateType.removed).all()
    return schema.dump(cases_query_result).data


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
    return tst_case_schema.dump(test_case).data


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
