from nested_lookup import nested_lookup

from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import create_test_case_cycle
from sherlock_back.api.data.model import Case, StateType, EntityType, Cycle


def self_parent_and_mismatch_check(project_id, cases_array, target_case):
    cases_id = [case['id'] for case in cases_array]

    if target_case in cases_array:
        return 'SELF_PARENT_ERROR'

    cases = Case.query.filter_by(project_id=project_id).filter(Case.id.in_(cases_id)).all()

    if len(cases) != len(cases_array):
        return 'CASE_PROJECT_MISMATCH'

    target_case_check = Case.query.filter_by(
        project_id=project_id).filter(Case.id == target_case).first()

    if target_case_check is None:
        return 'INVALID_TARGET_CASE'


def add_parent_id_to_cases(cases_array, project_id, target_case):
    cases_id = [case['id'] for case in cases_array]
    cases = Case.query.filter_by(
        project_id=project_id).filter(Case.id.in_(cases_id)).all()

    target_case = Case.query.filter_by(
        project_id=project_id).filter(Case.id == target_case).first()

    for case in cases:
        case.parent_id = target_case.id

        import pdb; pdb.set_trace()

        db.session.add(case)
        db.session.commit()


def remove_parent_id_from_cases(cases_array, project_id):
    cases = Case.query.filter_by(
        project_id=project_id).filter(Case.id.in_(cases_array)).all()

    for case in cases:
        case.parent_id = 0
        db.session.add(case)
        db.session.commit()


def create_test_case(test_case_text, parent_id, project_id, entity=EntityType.case):
    last_case = Case.query.filter_by(
        project_id=project_id).order_by(Case.order_index.desc()).first()

    if last_case:
        order_index = last_case.order_index + 1
    else:
        order_index = 1

    case = Case(
        name=test_case_text,
        parent_id=parent_id,
        project_id=project_id,
        entity=entity,
        order_index=order_index
    )
    db.session.add(case)
    db.session.commit()

    # UPDATE ONGOING CYCLE
    cycle = Cycle.query.filter_by(project_id=case.project_id).order_by('id').first()
    if cycle and cycle.state_code != StateType.closed:
        create_test_case_cycle(
            cycle_id=cycle.id,
            case_id=case.id,
            parent_id=case.parent_id
        )
